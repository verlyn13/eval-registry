#!/usr/bin/env python3
"""Reject mutations to versioned schemas and future append-only record paths."""

from __future__ import annotations

import subprocess
import sys

IMMUTABLE_PREFIXES = ("records/", "schemas/")


def path_is_immutable(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in IMMUTABLE_PREFIXES)


def changed_paths(base: str, head: str) -> list[tuple[str, str]]:
    process = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", "-z", f"{base}..{head}"],
        check=True,
        capture_output=True,
    )
    fields = process.stdout.decode("utf-8").split("\0")
    fields = [field for field in fields if field]
    if len(fields) % 2:
        raise ValueError("unexpected git diff field count")
    return list(zip(fields[0::2], fields[1::2], strict=True))


def violations(changes: list[tuple[str, str]]) -> list[str]:
    return [
        f"{status} {path}: immutable paths permit additions only"
        for status, path in changes
        if path_is_immutable(path) and status != "A"
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_append_only.py BASE_SHA HEAD_SHA", file=sys.stderr)
        return 2
    problems = violations(changed_paths(argv[1], argv[2]))
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print("append-only diff validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
