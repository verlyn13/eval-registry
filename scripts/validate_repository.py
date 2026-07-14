#!/usr/bin/env python3
"""Validate the inert D2 repository scaffold without external dependencies or I/O."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PATH_PARTS = {".git", ".ruff_cache", ".pytest_cache", "__pycache__"}

REQUIRED_FILES = {
    "README.md",
    "AGENTS.md",
    "policy/authorization-state.json",
    "docs/architecture.md",
    "docs/verification-policy.md",
    "docs/append-only-review.md",
    "docs/agent-identity-approval-roadmap.md",
    "schemas/registration-receipt.v1.schema.json",
    "schemas/attempt-disposition.v1.schema.json",
    "schemas/verification-result.v1.schema.json",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/validate.yml",
    "scripts/validate_pr_attestation.py",
}

GENERIC_PUBLIC_BOUNDARY_MARKERS = (
    "/" + "Users/",
    "/" + "home/",
    "C:" + "\\Users\\",
    "op:" + "//",
    "BEGIN " + "PRIVATE KEY",
    "BEGIN " + "OPENSSH PRIVATE KEY",
)

FORBIDDEN_D2_PREFIXES = ("records/", "receipts/", "dispositions/", "bundles/", "trust/")

FORBIDDEN_WORKFLOW_MARKERS = (
    "id-token: write",
    "cosign sign",
    "cosign attest",
    "rekor-cli",
    "openssl ts",
    "curl ",
    "wget ",
    "gh api",
    "secrets.",
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON number: {value}")
        ),
    )


def load_json(path: Path) -> Any:
    return parse_json_text(path.read_text(encoding="utf-8"))


def validate_authorization_state(value: Any) -> list[str]:
    expected = {
        "schema_version": "eval-registry.authorization-state.v1",
        "stage": "d2_scaffold",
        "repository_creation_approved": True,
        "pull_request_review_mode": "solo_maintainer_attestation_v1",
        "signer_workflow_approved": False,
        "external_authorities_approved": False,
        "record_publication_approved": False,
        "effective_date": "2026-07-13",
    }
    return (
        []
        if value == expected
        else ["authorization state is not the exact D2 scaffold state"]
    )


def is_record_path(relative_path: str) -> bool:
    return any(relative_path.startswith(prefix) for prefix in FORBIDDEN_D2_PREFIXES)


def _tracked_source_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not IGNORED_PATH_PARTS.intersection(path.relative_to(ROOT).parts)
        and path.suffix not in {".pyc", ".pyo"}
    )


def validate_repository() -> list[str]:
    errors: list[str] = []
    present = {path.relative_to(ROOT).as_posix() for path in _tracked_source_files()}

    missing = sorted(REQUIRED_FILES - present)
    errors.extend(f"missing required file: {path}" for path in missing)

    forbidden_files = sorted(path for path in present if is_record_path(path))
    errors.extend(
        f"D2 forbids record/trust material path: {path}" for path in forbidden_files
    )

    for relative in sorted(path for path in present if path.endswith(".json")):
        try:
            value = load_json(ROOT / relative)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid exact JSON in {relative}: {exc}")
            continue
        if relative.startswith("schemas/"):
            if not isinstance(value, dict):
                errors.append(f"schema is not an object: {relative}")
            elif value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"schema draft is not pinned in {relative}")
            elif value.get("additionalProperties") is not False:
                errors.append(f"top-level schema is not closed: {relative}")

    try:
        state = load_json(ROOT / "policy/authorization-state.json")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read authorization state: {exc}")
    else:
        errors.extend(validate_authorization_state(state))

    for path in _tracked_source_files():
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"binary/non-UTF-8 content is forbidden in D2: {relative}")
            continue
        for marker in GENERIC_PUBLIC_BOUNDARY_MARKERS:
            if marker.casefold() in text.casefold():
                errors.append(f"public-boundary marker in {relative}: {marker!r}")

        if relative.startswith(".github/workflows/"):
            lowered = text.casefold()
            for marker in FORBIDDEN_WORKFLOW_MARKERS:
                if marker.casefold() in lowered:
                    errors.append(
                        f"D2 workflow activation marker in {relative}: {marker!r}"
                    )

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("eval-registry D2 scaffold validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
