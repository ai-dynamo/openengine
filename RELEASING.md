<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine publishes its canonical Protobuf schema as `buf.build/openengine/openengine` and generated Rust bindings as the `openengine` crate on crates.io. Schema releases use `vMAJOR.MINOR.PATCH` tags; crate releases use separate `openengine-vMAJOR.MINOR.PATCH` tags so each crate can identify an already-published immutable BSR commit.

## Prepare a release

1. Confirm the schema revision documented in `proto/openengine/v1/README.md` and `docs/api.md`. The first valid revision is `1`; zero is invalid.
2. Update the release tag and status in `README.md`, `proto/buf.md`, and `proto/openengine/v1/README.md`. Keep the BSR commit as a placeholder until publication assigns it.
3. Validate the schema:

   ```bash
   buf format --diff --exit-code
   buf lint
   buf build
   ```

4. Open and merge the release-preparation pull request, then confirm the release commit is on `main` and all required checks passed.
5. Fetch `main` and check out the exact release commit. Release tags pointing outside `main` are rejected by the `Buf Push` workflow.

## Publish

Create and push a signed semantic-version tag from the release commit:

```bash
VERSION=v0.2.0
git tag --sign "${VERSION}" -m "OpenEngine ${VERSION}"
git push origin "${VERSION}"
```

The tag triggers the `Buf Push` workflow, which verifies that the tagged commit is on `main`, validates the schema, and publishes it to the BSR module. The Buf action derives labels from remote Git refs: the tag supplies the release label, and `main` is also applied when it still points to the exact release commit. Do not advance `main` until the publish workflow completes.

Maintainers may also run the workflow manually from `main`. A manual publication is immutable but does not replace a tagged release.

## Verify

1. Confirm the `Buf Push` workflow succeeded and record the immutable BSR module commit printed by the workflow.
2. Confirm the release and default labels are present:

   ```bash
   buf registry module label list buf.build/openengine/openengine
   buf registry module commit list buf.build/openengine/openengine:${VERSION}
   ```

3. Build the published commit directly:

   ```bash
   buf build buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
   ```

4. Inspect the BSR module landing page, generated schema documentation, source backlink, and Apache-2.0 license.
5. Generate bindings from the immutable commit with at least one representative consumer configuration.
6. Create the GitHub release for the signed tag. The release notes must record the Git commit, immutable BSR module commit, schema revision, compatibility status, and links to the BSR module and canonical schema.
7. Update downstream consumers to pin the immutable BSR module commit directly or through `buf.lock`. Engine implementations advertise that commit in `ServerInfo.schema_release`.
8. Update `README.md` and `proto/openengine/v1/README.md` on `main` with the immutable BSR commit assigned during publication.

Consumers may use release labels for discovery, but must not use a moving label as their production dependency.

## Release the Rust crate

### One-time registry configuration

The crate must exist before crates.io allows a Trusted Publisher to be configured. Bootstrap the first release as follows:

1. Create the `release` GitHub environment and protect it with the desired approval policy.
2. Prepare and merge the crate release commit using the process below.
3. Create the signed `openengine-vMAJOR.MINOR.PATCH` tag locally, but do not push it yet.
4. Create a short-lived crates.io token authorized to publish a new crate, publish from the tagged commit with `CARGO_REGISTRY_TOKEN=... cargo publish --locked --package openengine`, and immediately revoke the token.
5. Add the project maintainers or an `ai-dynamo` GitHub team as crate owners.
6. Configure a crates.io Trusted Publisher for GitHub owner `ai-dynamo`, repository `openengine`, workflow `rust-release.yml`, and environment `release`.
7. Push the signed tag. The workflow verifies that the existing crates.io archive matches the tagged source and skips a duplicate publication.

Subsequent releases use crates.io Trusted Publishing and do not require a stored registry token.

### Prepare a crate release

1. Identify the published schema release for the bindings. If the schema changed, publish and verify it through the BSR process above first.
2. Update the workspace package version in `Cargo.toml` and set `SCHEMA_RELEASE` in `packages/rust/openengine/src/lib.rs` to the immutable BSR module commit.
3. Regenerate and validate the package:

   ```bash
   ./scripts/generate-rust.sh
   ./scripts/check-generated.sh
   cargo check --locked --workspace --all-targets
   cargo clippy --locked --workspace --all-targets -- -D warnings
   cargo doc --locked --no-deps --package openengine
   cargo package --locked --package openengine
   ```

4. Update `CHANGELOG.md`, then open and merge the release-preparation pull request.

### Publish a crate release

Create and push a signed tag from the merged release commit:

```bash
VERSION=0.2.0
./scripts/check-release-version.sh "openengine-v${VERSION}"
git tag --sign "openengine-v${VERSION}" -m "OpenEngine Rust crate ${VERSION}"
git push origin "openengine-v${VERSION}"
```

The `Rust crate release` workflow verifies the tag, generated bindings, and packaged archive before obtaining a short-lived crates.io token through OpenID Connect and publishing the crate. Published crate versions cannot be replaced; yank a broken release and prepare a new patch version.
