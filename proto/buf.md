<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine

OpenEngine is a vendor-neutral gRPC protocol for coordinating inference engines and distributed frameworks. It keeps engine execution native while providing one typed runtime contract for inference, discovery, lifecycle, load, LoRA, and disaggregated KV-cache coordination.

> [!IMPORTANT]
> OpenEngine is experimental and pre-adoption. The contract may make direct breaking changes while it remains at schema revision `1`.

## Consume the schema

The canonical module is `buf.build/openengine/openengine`. Consumers own language-specific code generation and should pin an immutable BSR module commit rather than a moving label.

```bash
buf generate buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
```

Consumers that declare OpenEngine as a Protobuf dependency should commit the resulting `buf.lock` and keep generator plugins version-pinned in `buf.gen.yaml`.

Servers implementing this contract advertise `schema_revision = 1`, `minimum_client_revision = 1`, and the immutable BSR module commit in `ServerInfo.schema_release`.

## Resources

- [Canonical source](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
- [Human-readable API reference](https://github.com/ai-dynamo/openengine/blob/main/docs/api.md)
- [Motivation and adoption model](https://github.com/ai-dynamo/openengine/blob/main/docs/motivation.md)
- [Release process](https://github.com/ai-dynamo/openengine/blob/main/RELEASING.md)
- [Contributing](https://github.com/ai-dynamo/openengine/blob/main/CONTRIBUTING.md)
- [Security policy](https://github.com/ai-dynamo/openengine/blob/main/SECURITY.md)
- [Apache-2.0 license](https://github.com/ai-dynamo/openengine/blob/main/LICENSE)
