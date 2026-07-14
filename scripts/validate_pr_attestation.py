#!/usr/bin/env python3
"""Validate the temporary solo-maintainer review attestation on a pull request."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REVIEW_MODE = "solo_maintainer_attestation_v1"
START = "<!-- solo-maintainer-attestation:v1 -->"
END = "<!-- /solo-maintainer-attestation:v1 -->"
COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_DECLARATIONS = (
    "I reviewed the complete final diff at the recorded head SHA.",
    "I reviewed the public-content boundary and found no prohibited private material.",
    "I ran or verified the required repository checks for this exact revision.",
    "I disclosed scope limits, residual risks, and any unresolved concern.",
    "I understand this is solo-maintainer self-review, not independent approval.",
)
REQUIRED_FIELDS = {"review_mode", "reviewed_by", "reviewed_head_sha"}


class AttestationError(ValueError):
    """Raised when a pull-request attestation is missing, stale, or malformed."""


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise AttestationError(f"missing or invalid pull-request {label}")
    return value


def extract_block(body: str) -> str:
    if body.count(START) != 1 or body.count(END) != 1:
        raise AttestationError("expected exactly one solo-maintainer attestation block")
    before, remainder = body.split(START, 1)
    block, after = remainder.split(END, 1)
    if END in before or START in after:
        raise AttestationError("malformed solo-maintainer attestation markers")
    return block.strip()


def parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith("- ["):
            continue
        if ":" not in line:
            raise AttestationError(f"unexpected attestation line: {line!r}")
        key, value = (part.strip() for part in line.split(":", 1))
        if key not in REQUIRED_FIELDS:
            raise AttestationError(f"unexpected attestation field: {key!r}")
        if key in fields:
            raise AttestationError(f"duplicate attestation field: {key!r}")
        if not value:
            raise AttestationError(f"empty attestation field: {key!r}")
        fields[key] = value
    if set(fields) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(fields))
        raise AttestationError(f"missing attestation fields: {missing}")
    return fields


def validate_event(event: Any) -> None:
    if not isinstance(event, dict):
        raise AttestationError("GitHub event is not an object")
    pull_request = event.get("pull_request")
    if not isinstance(pull_request, dict):
        raise AttestationError("event is not a pull-request event")

    body = _string(pull_request.get("body"), "body")
    head = pull_request.get("head")
    author = pull_request.get("user")
    if not isinstance(head, dict) or not isinstance(author, dict):
        raise AttestationError("missing pull-request head or author")
    head_sha = _string(head.get("sha"), "head SHA").lower()
    author_login = _string(author.get("login"), "author login")
    if COMMIT_SHA_RE.fullmatch(head_sha) is None:
        raise AttestationError(
            "pull-request head SHA is not 40 lowercase hexadecimal characters"
        )

    block = extract_block(body)
    fields = parse_fields(block)
    if fields["review_mode"] != REVIEW_MODE:
        raise AttestationError(
            "review_mode does not match the authorized temporary mode"
        )
    if fields["reviewed_by"] != author_login:
        raise AttestationError("reviewed_by must equal the pull-request author login")
    if fields["reviewed_head_sha"] != head_sha:
        raise AttestationError(
            "reviewed_head_sha is stale or does not match the current head"
        )

    for declaration in REQUIRED_DECLARATIONS:
        checked = f"- [x] {declaration}"
        if block.count(checked) != 1:
            raise AttestationError(
                f"required declaration is missing or unchecked: {declaration}"
            )


def load_event(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: validate_pr_attestation.py GITHUB_EVENT_PATH", file=sys.stderr)
        return 2
    try:
        validate_event(load_event(Path(args[0])))
    except (OSError, UnicodeError, json.JSONDecodeError, AttestationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("solo-maintainer exact-head attestation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
