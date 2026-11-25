<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

Schema releases use `vMAJOR.MINOR.PATCH` tags and publish to the Buf Schema Registry (BSR) as `buf.build/openengine/openengine`. Rust crate releases use `openengine-vMAJOR.MINOR.PATCH` tags and package bindings for a published BSR commit.

## Prepare a release

1. Set the advertised revision in `proto/buf.md` using the inline declaration `schema_revision = N`. Confirm that `proto/openengine/v1/README.md` and `docs/api.md` agree. The first valid revision is `1`.
2. Update the release tag and status in `README.md`, `proto/buf.md`, and `proto/openengine/v1/README.md`. Until publication assigns the BSR commit, use `pending` in the release table and `${OPENENGINE_BSR_COMMIT}` in the Buf command.
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
6. Create the GitHub release for the signed tag. Record the Git commit, schema revision, compatibility status, and links to the BSR module and canonical schema. Label the registry identifier **Immutable BSR commit** and put its value in backticks, as in the [v0.1.0 release notes](https://github.com/ai-dynamo/openengine/releases/tag/v0.1.0).
7. Update downstream consumers to pin the immutable BSR module commit directly or through `buf.lock`. Engine implementations advertise that commit in `ServerInfo.schema_release`.
8. Put the published BSR commit in the `README.md` release table and Buf command. Docs CI checks both against the release notes for the table's Git tag. The Rust crate is checked against the release notes for its own schema tag.

Consumers may use release labels for discovery, but must not use a moving label as their production dependency.

## Release the Rust crate

### Prepare a crate release

1. Choose the published schema for the bindings and fetch its Git tag. Generation reads the proto files from the commit recorded in the crate manifest. To ship bindings for a newer schema, publish and verify that schema in the BSR first.
2. Update the workspace package version in `Cargo.toml` and the crate version, schema revision, immutable BSR module commit, Git tag, and Git commit in `packages/rust/openengine/schema-release.json`. Update the pinned schema link in `packages/rust/openengine/README.md`.
3. Refresh the workspace lockfile and regenerate the bindings.

   ```bash
   cargo metadata --format-version 1 > /dev/null
   ./scripts/generate-rust.sh
   ```

4. Add release notes under the crate version in [CHANGELOG.md](CHANGELOG.md), review the lockfile and generated changes, and commit the release preparation. From the clean checkout, verify the package.

   ```bash
   ./scripts/check-generated.sh
   ./scripts/check-schema-release.sh --verify-registry
   cargo check --locked --workspace --all-targets
   cargo test --locked --package openengine
   cargo clippy --locked --workspace --all-targets -- -D warnings
   cargo doc --locked --no-deps --package openengine
   cargo package --locked --package openengine
   ```

5. Open and merge the release-preparation pull request.

### Publish a crate release

Once release approvals are complete, check out the merged release commit. Create the signed crate tag and verify its signature.

```bash
VERSION=0.1.0
./scripts/check-release-version.sh "openengine-v${VERSION}"
git tag --sign "openengine-v${VERSION}" -m "OpenEngine Rust crate ${VERSION}"
git verify-tag "openengine-v${VERSION}"
```

Confirm that the reported signer is a trusted release maintainer before pushing the tag.

```bash
git push origin "openengine-v${VERSION}"
```

The maintainer owns signature verification. The `Rust crate release` workflow checks that the tagged commit is on `main`, matches the tag version to the crate, verifies the schema and generated bindings, and builds the archive. After these checks pass, a DevOps reviewer approves the publish job in the GitHub `release` environment. The job publishes the crate through crates.io Trusted Publishing. To correct a published release, yank it and prepare a new patch version.
