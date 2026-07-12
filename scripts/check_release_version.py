#!/usr/bin/env python3
"""Verify that a release tag matches every generated package version."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


def read_toml(path: Path) -> dict:
    with path.open("rb") as source:
        return tomllib.load(source)


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", sys.argv[1]):
        print("usage: check_release_version.py vMAJOR.MINOR.PATCH", file=sys.stderr)
        return 2

    repository = Path(__file__).resolve().parent.parent
    tag_version = sys.argv[1].removeprefix("v")
    python_version = read_toml(repository / "packages/python/pyproject.toml")["project"]["version"]
    rust_version = read_toml(repository / "Cargo.toml")["workspace"]["package"]["version"]

    versions = {
        "release tag": tag_version,
        "Python package": python_version,
        "Rust crate": rust_version,
    }
    if len(set(versions.values())) != 1:
        for label, version in versions.items():
            print(f"{label}: {version}", file=sys.stderr)
        return 1

    print(f"OpenEngine release versions match: {tag_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
