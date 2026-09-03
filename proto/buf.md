<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine

OpenEngine is a vendor-neutral gRPC protocol for coordinating inference engines and distributed frameworks. It keeps engine execution native while providing one typed runtime contract for inference, discovery, lifecycle, load, LoRA, and disaggregated KV-cache coordination.

> [!IMPORTANT]
> OpenEngine v0.1.0 is experimental and pre-adoption. The contract may make direct breaking changes while it remains at schema revision `1`.

## Consume the schema

The canonical module is `buf.build/openengine/openengine`. Consumers can use [BSR-generated SDKs](https://buf.build/docs/bsr/generated-sdks/) or generate bindings with their own version-pinned plugins. Rust users can install the first-party `openengine` crate.

Generate bindings from the immutable BSR commit recorded in the [v0.1.0 release](https://github.com/ai-dynamo/openengine/releases/tag/v0.1.0):

```bash
buf generate buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
```

Consumers that declare OpenEngine as a Protobuf dependency should commit the resulting `buf.lock` and keep generator plugins version-pinned in `buf.gen.yaml`. The `v0.1.0` label may be used for discovery, but production dependencies should pin the immutable commit.

Servers implementing this contract advertise `schema_revision = 1`, `minimum_client_revision = 1`, and the immutable BSR module commit in `ServerInfo.schema_release`.

## Resources

- [Canonical source](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
- [OpenEngine v0.1.0](https://github.com/ai-dynamo/openengine/releases/tag/v0.1.0)
- [Human-readable API reference](https://github.com/ai-dynamo/openengine/blob/main/docs/api.md)
- [Motivation and adoption model](https://github.com/ai-dynamo/openengine/blob/main/docs/motivation.md)
- [Release process](https://github.com/ai-dynamo/openengine/blob/main/RELEASING.md)
- [Contributing](https://github.com/ai-dynamo/openengine/blob/main/CONTRIBUTING.md)
- [Security policy](https://github.com/ai-dynamo/openengine/blob/main/SECURITY.md)
- [Apache-2.0 license](https://github.com/ai-dynamo/openengine/blob/main/LICENSE)
