<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine publishes the canonical schema and generated Python and Rust
bindings from the same `vMAJOR.MINOR.PATCH` tag. Releases are immutable and all
published artifacts must use the same version.

## One-time repository configuration

Before the first release:

1. Register `openengine-proto` on PyPI and crates.io.
2. Configure a PyPI Trusted Publisher for the `Release` workflow, the
   `publish-python` job, and the `release` GitHub environment.
3. Add a crates.io publishing token as the `CARGO_REGISTRY_TOKEN` environment
   secret.
4. Protect the `release` GitHub environment with the desired approval policy.
5. Add the appropriate project owners on both registries.

The PyPI job uses OpenID Connect and does not require a stored PyPI token.

## Prepare a release

1. Choose the release version and update both version declarations:
   - `packages/python/pyproject.toml` under `[project]`.
   - `Cargo.toml` under `[workspace.package]`.
2. Move the relevant entries from `Unreleased` in `CHANGELOG.md` into a section
   named for the version and release date.
3. Install the pinned Python generator and regenerate bindings:

   ```bash
   python -m pip install grpcio-tools==1.81.1
   ./scripts/generate-python.sh
   ./scripts/generate-rust.sh
   ```

4. Run the package checks:

   ```bash
   ./scripts/check-generated.sh
   cargo test --locked --package openengine-proto
   cargo package --locked --package openengine-proto
   python -m build packages/python --outdir dist/python
   python -m twine check dist/python/*
   ./scripts/test-cross-language.sh
   ```

5. Open and merge the release-preparation pull request.

## Publish

Create and push a signed tag from the release commit:

```bash
python scripts/check_release_version.py v0.1.0
git tag --sign v0.1.0 -m "OpenEngine v0.1.0"
git push origin v0.1.0
```

The `Release` workflow validates the schema, regenerates and tests both
packages, publishes them, and creates a GitHub release containing:

- The Python wheel and source distribution.
- The packaged Rust crate.
- The canonical proto source archive.
- The complete protobuf descriptor set.
- SHA-256 checksums.

If publication fails after one registry accepts a package, do not overwrite or
delete that artifact. Fix the workflow and rerun only if the remaining steps
are safe, or prepare a new patch release.
