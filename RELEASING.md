<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine publishes its Protobuf schema as `buf.build/openengine/openengine`. The project does not currently maintain first-party language packages. Consumers may use BSR-generated SDKs or generate bindings with their own version-pinned plugins from an immutable BSR module commit.

## Prepare a release

1. Confirm the schema revision documented in `proto/openengine/v1/README.md` and `docs/api.md`. The first valid revision is `1`; zero is invalid.
2. Describe the changes since the previous release in `README.md` and `proto/openengine/v1/README.md`. The registry stores `proto/buf.md` with each immutable module commit, so its installation instructions should point readers to the notes for their chosen release.
3. Validate the schema:

   ```bash
   buf format --diff --exit-code
   buf lint
   buf build
   buf breaking --against '.git#ref=b5f2bd93721f7b888d3e2440679e0ae7012939d1'
   ```

   Fetch the full repository history and tags before checking compatibility. The command above and the Buf Push workflow use the published v0.1.0 commit as their baseline; advance both after publication. Fix compatibility failures without relaxing the deletion rules. Generate bindings with a representative consumer configuration and check the resulting imports. For comment-only schema edits, compare descriptors generated without source information before and after the change.

4. Open and merge the release-preparation pull request, then confirm the release commit is on `main` and all required checks passed.
5. Fetch `main` and check out the exact release commit. Release tags pointing outside `main` are rejected by the `Buf Push` workflow.

## Publish

Set `VERSION` to the chosen tag (in `vMAJOR.MINOR.PATCH` format), then create and push the signed tag from the release commit.

```bash
: "${VERSION:?Set VERSION to the release tag}"
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

3. Set `OPENENGINE_BSR_COMMIT` to the commit recorded in step 1, then build it:

   ```bash
   buf build buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
   ```

4. Inspect the BSR module landing page, generated schema documentation, source backlink, and Apache-2.0 license.
5. Generate bindings from the immutable commit with at least one representative consumer configuration.
6. Create the GitHub release for the signed tag. Record the Git commit, immutable BSR module commit, schema revision, compatibility status, and links to the BSR module and schema in the release notes. Describe multimodal and other optional feature support per engine.
7. Update downstream consumers to pin the immutable BSR module commit directly or through `buf.lock`. Engine implementations advertise that commit in `ServerInfo.schema_release`.
8. Update the release badge, status, artifact table, and binding generation example in `README.md` on `main` with the published version and its immutable BSR commit.
9. Advance `breaking_against` in the Buf Push workflow and the documented local compatibility command to the newly published Git commit. Keep published tags and BSR commits immutable.

Consumers may use release labels for discovery, but must not use a moving label as their production dependency.
