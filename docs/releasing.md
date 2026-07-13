<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Releasing the OpenEngine schema

OpenEngine is released as the public `buf.build/ai-dynamo/openengine` module.
The complete `proto/` tree is one atomic release unit; this repository does not
need to publish or version a Python module, Rust crate, or other language
package.

## One-time repository setup

1. Ensure the `ai-dynamo` organization exists on the public Buf Schema
   Registry.
2. Create a Buf token that can create and push the `openengine` module in that
   organization.
3. Add the token to this GitHub repository as an Actions secret named
   `BUF_TOKEN`.

The first authorized push creates the BSR repository with public visibility.
No language-specific code generation configuration is required to publish the
schema.

## Continuous publication

The Buf workflow validates builds, lint, formatting, and `FILE` compatibility
on pull requests. A merge to `main` publishes the corresponding immutable BSR
commit on the `main` label. Deleting a Git branch or tag archives its matching
BSR label.

Before merging a schema change:

```bash
buf build
buf lint
buf format --diff --exit-code
buf breaking --against '.git#branch=main'
```

The `FILE` policy is intentional: OpenEngine distributes source schemas, and
moving an existing declaration between files can break generated Python or C++
code even when the protobuf wire representation is unchanged.

## Versioned releases

1. Confirm the intended release commit has successfully published to the BSR
   `main` label.
2. Choose a semantic version and create an annotated tag at that exact commit.
3. Push the tag to GitHub.
4. Confirm the Buf workflow publishes the same schema under the matching BSR
   version label.

For example:

```bash
git tag -a v1.0.0 -m "OpenEngine v1.0.0"
git push origin v1.0.0
```

Servers built from a versioned release should advertise that immutable tag in
`EngineInfo.schema_release`. Consumers can reference the release label in
`buf.yaml`; committing `buf.lock` pins the label to its content-addressed BSR
commit and digest.

Do not move an existing version tag. Corrections require a new patch release.
An incompatible API change requires both a new semantic major version and a new
versioned Protobuf package such as `openengine.v2`.
