<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# SPDX headers

Every tracked source, document, and configuration file must carry a leading SPDX copyright and license header. NVIDIA-authored files use the following text in their language's comment syntax; shell scripts keep the shebang first.

```text
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
```

Rust and Protobuf use `//` comments; shell, Python, TOML, YAML, and Git configuration use `#` comments. Markdown accepts the existing multiline HTML comment or two standalone HTML comments. Copyright year ranges are accepted. New file types fail validation until their comment syntax or asset policy is reviewed.

## Generated files and assets

Generated Rust carries the same header as handwritten Rust. The Rust generator must reproduce it, and `scripts/check-generated.sh` checks for drift when the Rust package is present.

The exact paths below use adjacent, tracked `.license` files containing the two SPDX lines without comment markers. A missing, malformed, untracked, or orphaned sidecar fails validation. These paths are checked when present; no extension-wide exemption applies.

- `Cargo.lock`: Cargo-managed dependency lockfile.
- `docs/assets/logo.png`: binary project logo.
- `packages/rust/openengine/schema-release.json`: JSON schema metadata.
- `packages/rust/openengine/src/generated/openengine_descriptor.bin`: generated binary descriptor.

The canonical `LICENSE` and `LICENSES/CC-BY-4.0.txt` are standard license texts and remain unmodified by header insertion. They are the only header exemptions.

## Third-party attribution

`CODE_OF_CONDUCT.md` retains its Contributor Covenant attribution and uses `SPDX-FileCopyrightText: Contributor Covenant contributors` and `SPDX-License-Identifier: CC-BY-4.0`. Its source identifies Contributor Covenant version 2.1. The [upstream license before the version 3 site redesign](https://raw.githubusercontent.com/ContributorCovenant/contributor_covenant/91532d80ea5f39b6685aff4892bc6854bf2f6d6f/LICENSE.md) is CC-BY-4.0; the license text is included under `LICENSES/`. This document is not relabeled as NVIDIA-authored Apache-2.0 source. New third-party files need their applicable attribution and an explicit checker rule.

## Run the check

The checker and tests use only the Python standard library (Python 3.9 or later).

```bash
python3 -m unittest discover -s tests -p test_spdx_headers.py
python3 scripts/check_spdx_headers.py
```

The scan enumerates `git ls-files`, including hidden files and sidecars. Stage new files before running it locally. Build output and untracked files are outside the scan; inspect the packaged crate separately when changing distribution contents.

The `SPDX headers` job in the `Compliance` GitHub Actions workflow runs for every pull request, pushes to `main`, and merge groups, without path filters. It is a required GitHub Actions check on `main`, alongside DCO and `Cargo deny`. See [dependency compliance](compliance.md) for the Cargo policy.

The workflow, checker, and initial tests are adapted from `ai-dynamo/governance` at commit `0f5dbdbf1c5f49a7a4265ab15a822301628e5bbd`. OpenEngine adds Rust/Protobuf/shell support, existing Markdown block support, reviewed sidecars, and the Contributor Covenant attribution rule. This check validates source attribution; it does not replace dependency license review or release approval.
