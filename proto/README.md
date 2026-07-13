<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine Protobuf module

OpenEngine is a vendor-neutral gRPC protocol for coordinating inference engines
and distributed frameworks. This directory is the root of the public
`buf.build/ai-dynamo/openengine` module.

The complete module is released atomically. Its canonical API is the
`openengine.v1` package under `openengine/v1/`; `openengine/v1/openengine.proto`
declares the service and imports request and response messages from the other
domain files.

## Consume with Buf

Add the module to the consuming workspace's `buf.yaml`:

```yaml
version: v2

deps:
  - buf.build/ai-dynamo/openengine
```

Run `buf dep update` and commit the resulting `buf.lock` for reproducible
builds. A semantic release label or immutable BSR commit can also be appended
to the dependency reference.

Generate language bindings from the module with the consumer's own
`buf.gen.yaml`. OpenEngine does not require consumers to install a project-owned
Python module, Rust crate, or other language package.

See the [repository documentation](https://github.com/ai-dynamo/openengine) for
the API reference, design motivation, and contribution process.

## Compatibility

The module uses Buf's `FILE` breaking-change policy. Existing declarations in
`openengine.v1` remain in their published files so generated source stays
compatible across languages, including Python and C++.
