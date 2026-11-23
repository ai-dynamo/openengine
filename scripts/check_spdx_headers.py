# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Validate SPDX headers and reviewed file-specific attributions."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


# Standard license text is preserved verbatim. No source files are exempt.
EXEMPT_PATHS = {Path("LICENSE"), Path("LICENSES/CC-BY-4.0.txt")}
# Exact non-commentable/generated assets use REUSE-compatible .license sidecars.
SIDECAR_PATHS = {
    Path("Cargo.lock"),
    Path("docs/assets/logo.png"),
    Path("packages/rust/openengine/schema-release.json"),
    Path("packages/rust/openengine/src/generated/openengine_descriptor.bin"),
}
HTML_SUFFIXES = {".md"}
HASH_SUFFIXES = {".py", ".toml", ".yaml", ".yml", ".sh"}
HASH_FILENAMES = {
    ".dockerignore",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "CODEOWNERS",
    "Dockerfile",
}
YEAR_PATTERN = r"\d{4}(?:-\d{4})?"
COPYRIGHT_TEXT = (
    r"SPDX-FileCopyrightText: Copyright \(c\) "
    rf"{YEAR_PATTERN} NVIDIA CORPORATION & AFFILIATES\. All rights reserved\."
)
LICENSE_TEXT = r"SPDX-License-Identifier: Apache-2\.0"
HASH_COPYRIGHT_RE = re.compile(rf"^# {COPYRIGHT_TEXT}$")
HASH_LICENSE_RE = re.compile(rf"^# {LICENSE_TEXT}$")
HTML_COPYRIGHT_RE = re.compile(rf"^<!-- {COPYRIGHT_TEXT} -->$")
HTML_LICENSE_RE = re.compile(rf"^<!-- {LICENSE_TEXT} -->$")


def header_patterns(path: Path) -> tuple[re.Pattern[str], re.Pattern[str]] | None:
    """Return the required header patterns for a supported path."""
    if path == Path("CODE_OF_CONDUCT.md"):
        return (
            re.compile(
                r"^<!-- SPDX-FileCopyrightText: Contributor Covenant contributors -->$"
            ),
            re.compile(r"^<!-- SPDX-License-Identifier: CC-BY-4\.0 -->$"),
        )
    if path.suffix.lower() in {".rs", ".proto"}:
        return re.compile(rf"^// {COPYRIGHT_TEXT}$"), re.compile(
            rf"^// {LICENSE_TEXT}$"
        )
    if path.suffix.lower() == ".license":
        return re.compile(rf"^{COPYRIGHT_TEXT}$"), re.compile(rf"^{LICENSE_TEXT}$")
    if path.suffix.lower() == ".mmd":
        return re.compile(rf"^%% {COPYRIGHT_TEXT}$"), re.compile(
            rf"^%% {LICENSE_TEXT}$"
        )
    if path.suffix.lower() in HTML_SUFFIXES:
        return HTML_COPYRIGHT_RE, HTML_LICENSE_RE
    if path.suffix.lower() in HASH_SUFFIXES or path.name in HASH_FILENAMES:
        return HASH_COPYRIGHT_RE, HASH_LICENSE_RE
    return None


def validate_file(root: Path, relative_path: Path) -> list[str]:
    """Return every SPDX policy violation found in one repository file."""
    if relative_path in EXEMPT_PATHS:
        return []

    path = root / relative_path
    if path.is_symlink():
        return [f"{relative_path}: symbolic links require an explicit policy"]
    if relative_path in SIDECAR_PATHS:
        if not path.is_file():
            return [f"{relative_path}: sidecar target does not exist"]
        return validate_file(root, Path(f"{relative_path}.license"))
    if relative_path.suffix == ".license":
        target = Path(str(relative_path).removesuffix(".license"))
        if target not in SIDECAR_PATHS or not (root / target).is_file():
            return [f"{relative_path}: unapproved or missing sidecar target"]

    patterns = header_patterns(relative_path)
    if patterns is None:
        return [f"{relative_path}: unsupported tracked file type"]

    path = root / relative_path
    try:
        contents = path.read_bytes()
    except OSError as error:
        return [f"{relative_path}: cannot read file: {error}"]
    if b"\x00" in contents:
        return [f"{relative_path}: binary files require an explicit policy"]
    try:
        lines = contents.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return [f"{relative_path}: file is not valid UTF-8 text"]

    # Existing documentation uses a single multiline HTML comment.
    if relative_path.suffix.lower() in HTML_SUFFIXES and lines[:1] == ["<!--"]:
        if len(lines) < 4 or "-->" not in lines[3:]:
            return [f"{relative_path}: malformed SPDX HTML header"]
        lines = [f"<!-- {lines[1]} -->", f"<!-- {lines[2]} -->"] + lines[
            lines.index("-->", 3) + 1 :
        ]
    start = 1 if lines and lines[0].startswith("#!/") else 0
    if len(lines) <= start:
        return [f"{relative_path}: missing NVIDIA copyright header"]
    if not patterns[0].fullmatch(lines[start]):
        return [f"{relative_path}: malformed or missing required copyright header"]
    if len(lines) <= start + 1 or not patterns[1].fullmatch(lines[start + 1]):
        return [f"{relative_path}: malformed or missing required license header"]
    return []


def validate_paths(root: Path, paths: Iterable[Path]) -> list[str]:
    """Return SPDX violations for all supplied repository-relative paths."""
    violations: list[str] = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        violations.extend(validate_file(root, path))
    return violations


def tracked_files(root: Path) -> list[Path]:
    """Return every path recorded in the repository index."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [Path(path) for path in result.stdout.decode("utf-8").split("\0") if path]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the SPDX checker."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root containing the tracked files",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the repository and return a process-compatible status code."""
    args = parse_args(argv)
    root = args.root.resolve()
    try:
        paths = tracked_files(root)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as error:
        print(f"unable to enumerate tracked files: {error}", file=sys.stderr)
        return 2

    path_set = set(paths)
    untracked_sidecars = [
        f"{path}: SPDX sidecar is not tracked"
        for path in paths
        if path in SIDECAR_PATHS and Path(f"{path}.license") not in path_set
    ]
    violations = untracked_sidecars + validate_paths(root, paths)
    if violations:
        print("SPDX header violations:", file=sys.stderr)
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 1
    print(f"Validated SPDX headers for {len(paths)} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
