#!/usr/bin/env python3
"""Verify that every release artifact carries the repository license text."""

from __future__ import annotations

import argparse
import tarfile
import zipfile
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
EXPECTED_LICENSE = (REPOSITORY / "LICENSE").read_bytes()


def check_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        licenses = [name for name in archive.namelist() if name.endswith("/LICENSE")]
        if len(licenses) != 1:
            raise RuntimeError(f"{path} contains {len(licenses)} LICENSE files")
        actual = archive.read(licenses[0])
    if actual != EXPECTED_LICENSE:
        raise RuntimeError(f"{path}:{licenses[0]} does not match the repository LICENSE")


def check_tar(path: Path) -> None:
    with tarfile.open(path, mode="r:*") as archive:
        licenses = [
            member
            for member in archive.getmembers()
            if member.isfile() and member.name.endswith("/LICENSE")
        ]
        if len(licenses) != 1:
            raise RuntimeError(f"{path} contains {len(licenses)} LICENSE files")
        source = archive.extractfile(licenses[0])
        if source is None:
            raise RuntimeError(f"cannot read {path}:{licenses[0].name}")
        actual = source.read()
    if actual != EXPECTED_LICENSE:
        raise RuntimeError(
            f"{path}:{licenses[0].name} does not match the repository LICENSE"
        )


def require_artifacts(pattern: str) -> list[Path]:
    artifacts = sorted(REPOSITORY.glob(pattern))
    if not artifacts:
        raise RuntimeError(f"no artifacts matched {pattern}")
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--python-only", action="store_true")
    scope.add_argument("--rust-only", action="store_true")
    args = parser.parse_args()

    if not args.rust_only:
        for wheel in require_artifacts("dist/python/*.whl"):
            check_zip(wheel)
        for source_distribution in require_artifacts("dist/python/*.tar.gz"):
            check_tar(source_distribution)

    if not args.python_only:
        for crate in require_artifacts("target/package/openengine-proto-*.crate"):
            check_tar(crate)

    print("OpenEngine package artifacts contain the canonical LICENSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
