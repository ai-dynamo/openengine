<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing OpenEngine

OpenEngine publishes its canonical Protobuf schema as
`buf.build/openengine/openengine`. The repository does not publish
language-specific packages. Consumers generate bindings with their own
version-pinned plugins from an immutable BSR module commit.

## Prepare a release

1. Confirm the schema revision in `proto/openengine/v1/version.proto`. The first
   valid revision is `1`; zero is invalid.
2. Move the relevant entries from `Unreleased` in `CHANGELOG.md` into a section
   named for the release version and date.
3. Validate the schema:

   ```bash
   buf format --diff --exit-code
   buf lint
   buf build
   ```

4. Open and merge the release-preparation pull request.

## Publish

Create and push a signed semantic-version tag from the release commit:

```bash
git tag --sign v0.1.0 -m "OpenEngine v0.1.0"
git push origin v0.1.0
```

The tag triggers the `Buf Push` workflow, which validates and publishes the
schema to the BSR module. Confirm the workflow succeeded and record the
resulting immutable BSR module commit in the release notes.

Maintainers may also run the workflow manually from `main`. A manual
publication is immutable but does not replace a tagged release.

Consumers may use release labels for discovery, but must pin the immutable BSR
module commit directly or through `buf.lock`. Engine implementations advertise
that commit in `ServerInfo.schema_release`.
