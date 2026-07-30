<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine publishes its canonical Protobuf schema as `buf.build/openengine/openengine`. The repository does not publish language-specific packages. Consumers generate bindings with their own version-pinned plugins from an immutable BSR module commit.

## Prepare a release

1. Confirm the schema revision documented in `proto/openengine/v1/README.md` and `docs/api.md`. The first valid revision is `1`; zero is invalid.
2. Validate the schema:

   ```bash
   buf format --diff --exit-code
   buf lint
   buf build
   ```

3. Open and merge the release-preparation pull request, then confirm the release commit is on `main` and all required checks passed.
4. Fetch `main` and check out the exact release commit. Release tags pointing outside `main` are rejected by the `Buf Push` workflow.

## Publish

Create and push a signed semantic-version tag from the release commit:

```bash
git tag --sign v0.1.0 -m "OpenEngine v0.1.0"
git push origin v0.1.0
```

The tag triggers the `Buf Push` workflow, which verifies that the tagged commit is on `main`, validates the schema, and publishes it to the BSR module. The Buf action derives labels from remote Git refs: the tag supplies the `v0.1.0` label, and `main` is also applied when it still points to the exact release commit. Do not advance `main` until the publish workflow completes.

Maintainers may also run the workflow manually from `main`. A manual publication is immutable but does not replace a tagged release.

## Verify

1. Confirm the `Buf Push` workflow succeeded and record the immutable BSR module commit printed by the workflow.
2. Confirm the release and default labels are present:

   ```bash
   buf registry module label list buf.build/openengine/openengine
   buf registry module commit list buf.build/openengine/openengine:v0.1.0
   ```

3. Build the published commit directly:

   ```bash
   buf build buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
   ```

4. Inspect the BSR module landing page, generated schema documentation, source backlink, and Apache-2.0 license.
5. Generate bindings from the immutable commit with at least one representative consumer configuration.
6. Create the GitHub release for the signed tag. The release notes must record the Git commit, immutable BSR module commit, schema revision, compatibility status, and links to the BSR module and canonical schema.
7. Update downstream consumers to pin the immutable BSR module commit directly or through `buf.lock`. Engine implementations advertise that commit in `ServerInfo.schema_release`.

Consumers may use release labels for discovery, but must not use a moving label as their production dependency.
