<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine builds the canonical schema and generated Python and Rust bindings
from the same `vMAJOR.MINOR.PATCH` tag. Releases are immutable and all artifacts
use the same version. Initial consumers use local path or immutable Git commit
dependencies; publication to PyPI and crates.io is intentionally deferred.

Release tooling requires Python 3.11 or newer.

## Prepare a release

1. Choose the release version and update both version declarations:
   - `packages/python/pyproject.toml` under `[project]`.
   - `Cargo.toml` under `[workspace.package]`.
2. Move the relevant entries from `Unreleased` in `CHANGELOG.md` into a section
   named for the version and release date.
3. Install the pinned Python generator and regenerate bindings:

   ```bash
   python -m pip install build==1.3.0 grpcio-tools==1.81.1 twine==6.2.0
   ./scripts/generate-python.sh
   ./scripts/generate-rust.sh
   ```

4. Run the package checks:

   ```bash
   ./scripts/check-generated.sh
   cargo test --locked --package openengine-proto
   cargo package --allow-dirty --locked --package openengine-proto
   python -m build packages/python --outdir dist/python
   python -m twine check dist/python/*
   python scripts/check_package_contents.py
   ./scripts/test-cross-language.sh
   ```

5. Open and merge the release-preparation pull request.

## Publish

Create and push a signed tag from the release commit:

```bash
python scripts/check_release_version.py v0.3.0
git tag --sign v0.3.0 -m "OpenEngine v0.3.0"
git push origin v0.3.0
```

The `Release` workflow validates the schema, regenerates and tests both
packages, and creates a GitHub release containing:

- The Python wheel and source distribution.
- The packaged Rust crate.
- The canonical proto source archive.
- The complete protobuf descriptor set.
- SHA-256 checksums.

Registry publication can be added later without changing package names or the
coordinated versioning rule.
