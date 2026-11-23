# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the repository-wide SPDX header validator."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).parents[1]


def load_checker() -> ModuleType:
    """Load the checker script as a module without packaging it."""
    path = ROOT / "scripts/check_spdx_headers.py"
    spec = importlib.util.spec_from_file_location("check_spdx_headers", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load SPDX checker from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()
HASH_HEADER = (
    "# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & "
    "AFFILIATES. All rights reserved.\n"
    "# SPDX-License-Identifier: Apache-2.0\n"
)
HTML_HEADER = (
    "<!-- SPDX-FileCopyrightText: Copyright (c) 2024-2026 NVIDIA CORPORATION & "
    "AFFILIATES. All rights reserved. -->\n"
    "<!-- SPDX-License-Identifier: Apache-2.0 -->\n"
)


class SpdxHeaderTests(unittest.TestCase):
    """Exercise supported headers, exemptions, and failure reporting."""

    def test_hash_header_is_accepted(self) -> None:
        """A supported hash-comment file accepts a single copyright year."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.py").write_text(HASH_HEADER, encoding="utf-8")
            self.assertEqual(CHECKER.validate_file(root, Path("example.py")), [])

    def test_markdown_year_range_is_accepted(self) -> None:
        """A Markdown header accepts an inclusive copyright year range."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(HTML_HEADER, encoding="utf-8")
            self.assertEqual(CHECKER.validate_file(root, Path("README.md")), [])

    def test_shebang_may_precede_header(self) -> None:
        """An executable script may place its shebang before the SPDX lines."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tool.py").write_text(
                "#!/usr/bin/env python3\n" + HASH_HEADER,
                encoding="utf-8",
            )
            self.assertEqual(CHECKER.validate_file(root, Path("tool.py")), [])

    def test_only_root_license_is_exempt(self) -> None:
        """The canonical root license is exempt while nested licenses are not."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(CHECKER.validate_file(root, Path("LICENSE")), [])
            self.assertIn(
                "unsupported tracked file type",
                CHECKER.validate_file(root, Path("vendor/LICENSE"))[0],
            )

    def test_binary_and_unknown_files_are_rejected(self) -> None:
        """Binary content and unsupported extensions require reviewed policy."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "binary.py").write_bytes(b"\x00data")
            (root / "unknown.txt").write_text("data", encoding="utf-8")
            self.assertIn(
                "binary files",
                CHECKER.validate_file(root, Path("binary.py"))[0],
            )
            self.assertIn(
                "unsupported tracked file type",
                CHECKER.validate_file(root, Path("unknown.txt"))[0],
            )

    def test_all_paths_are_reported(self) -> None:
        """Validation reports every offending path instead of stopping early."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.py").write_text("print('a')\n", encoding="utf-8")
            (root / "b.yaml").write_text("value: b\n", encoding="utf-8")
            violations = CHECKER.validate_paths(
                root,
                [Path("b.yaml"), Path("a.py")],
            )
            self.assertEqual(len(violations), 2)
            self.assertTrue(violations[0].startswith("a.py:"))
            self.assertTrue(violations[1].startswith("b.yaml:"))

    def test_sidecars_are_limited_to_reviewed_paths(self) -> None:
        """Reviewed assets need valid sidecars; arbitrary files cannot bypass checks."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = Path("Cargo.lock")
            (root / path).write_text("# generated lockfile\n", encoding="utf-8")
            self.assertTrue(CHECKER.validate_file(root, path))
            (root / "Cargo.lock.license").write_text(
                HASH_HEADER.replace("# ", ""), encoding="utf-8"
            )
            self.assertEqual(CHECKER.validate_file(root, path), [])
            (root / "Cargo.lock.license").write_text("SPDX-License-Identifier: MIT\n")
            self.assertTrue(CHECKER.validate_file(root, path))
            (root / "other.png.license").write_text(HASH_HEADER.replace("# ", ""))
            self.assertTrue(CHECKER.validate_file(root, Path("other.png.license")))
            self.assertTrue(CHECKER.validate_file(root, Path("other.png")))

    def test_orphan_sidecar_is_rejected(self) -> None:
        """A sidecar is meaningful only while its reviewed target exists."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Cargo.lock.license").write_text(HASH_HEADER.replace("# ", ""))
            self.assertTrue(CHECKER.validate_file(root, Path("Cargo.lock.license")))

    def test_multiline_markdown_header_is_accepted(self) -> None:
        """The repository's existing HTML block headers remain valid."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = "<!--\n" + HASH_HEADER.replace("# ", "") + "-->\n"
            (root / "README.md").write_text(header)
            self.assertEqual(CHECKER.validate_file(root, Path("README.md")), [])
            (root / "README.md").write_text(
                header.replace("-->\n", "\nLicensed under Apache 2.0.\n-->\n")
            )
            self.assertEqual(CHECKER.validate_file(root, Path("README.md")), [])
            (root / "README.md").write_text(header.replace("-->\n", ""))
            self.assertTrue(CHECKER.validate_file(root, Path("README.md")))

    def test_rust_and_proto_headers_are_accepted(self) -> None:
        """Rust inner attributes are not mistaken for an executable shebang."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = HASH_HEADER.replace("# ", "// ")
            for name in ("lib.rs", "api.proto"):
                (root / name).write_text(header)
                self.assertEqual(CHECKER.validate_file(root, Path(name)), [])
            (root / "lib.rs").write_text("#![allow(dead_code)]\n" + header)
            self.assertTrue(CHECKER.validate_file(root, Path("lib.rs")))

    def test_license_must_be_complete_and_at_top(self) -> None:
        """A body string or a non-Apache SPDX expression cannot satisfy the gate."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for header in (
                HASH_HEADER.replace("Apache-2.0", "Apache-2.0 OR MIT"),
                "print('body')\n" + HASH_HEADER,
                HASH_HEADER.replace("Apache-2.0", "MIT"),
            ):
                (root / "tool.py").write_text(header)
                self.assertTrue(CHECKER.validate_file(root, Path("tool.py")))

    def test_mermaid_source_requires_spdx_comments(self) -> None:
        """Diagram sources carry SPDX rather than inheriting a binary exemption."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = Path("flow.mmd")
            (root / path).write_text(
                HASH_HEADER.replace("# ", "%% ") + "flowchart TD\n", encoding="utf-8"
            )
            self.assertEqual(CHECKER.validate_file(root, path), [])
            (root / path).write_text("flowchart TD\n", encoding="utf-8")
            self.assertTrue(CHECKER.validate_file(root, path))

    def test_git_index_supplies_the_scan_set(self) -> None:
        """Only paths recorded by Git are returned for repository validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "tracked.py").write_text(HASH_HEADER, encoding="utf-8")
            (root / "untracked.py").write_text(HASH_HEADER, encoding="utf-8")
            subprocess.run(["git", "add", "tracked.py"], cwd=root, check=True)
            self.assertEqual(CHECKER.tracked_files(root), [Path("tracked.py")])

    def test_contributor_covenant_retains_its_license(self) -> None:
        """The third-party conduct policy cannot be relabeled as NVIDIA Apache."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            p = root / "CODE_OF_CONDUCT.md"
            p.write_text(
                "<!--\nSPDX-FileCopyrightText: Contributor Covenant contributors\n"
                "SPDX-License-Identifier: CC-BY-4.0\n-->\n"
            )
            self.assertEqual(CHECKER.validate_file(root, Path(p.name)), [])
            p.write_text(HTML_HEADER)
            self.assertTrue(CHECKER.validate_file(root, Path(p.name)))

    def test_main_requires_sidecar_to_be_tracked(self) -> None:
        """An ignored or untracked local sidecar cannot make CI appear compliant."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "Cargo.lock").write_text("# generated\n")
            (root / "Cargo.lock.license").write_text(HASH_HEADER.replace("# ", ""))
            subprocess.run(["git", "add", "Cargo.lock"], cwd=root, check=True)
            self.assertEqual(CHECKER.main(["--root", str(root)]), 1)
            subprocess.run(["git", "add", "Cargo.lock.license"], cwd=root, check=True)
            self.assertEqual(CHECKER.main(["--root", str(root)]), 0)


if __name__ == "__main__":
    unittest.main()
