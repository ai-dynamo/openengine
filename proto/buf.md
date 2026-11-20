<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine

OpenEngine is a vendor-neutral gRPC protocol for coordinating inference engines and distributed frameworks. It keeps engine execution native while providing one typed runtime contract for inference, discovery, lifecycle, load, LoRA, and disaggregated KV-cache coordination.

## Consume the schema

The module is `buf.build/openengine/openengine`. Consumers can use [BSR-generated SDKs](https://buf.build/docs/bsr/generated-sdks/) or generate bindings with their own version-pinned plugins. OpenEngine does not currently maintain first-party language packages.

Choose your version from the [OpenEngine releases](https://github.com/ai-dynamo/openengine/releases). Set `OPENENGINE_BSR_COMMIT` to the immutable BSR module commit listed in that release's notes, then generate bindings with your `buf.gen.yaml`.

```bash
buf generate buf.build/openengine/openengine:${OPENENGINE_BSR_COMMIT}
```

If you declare OpenEngine as a Protobuf dependency, pin the module commit, commit the resulting `buf.lock`, and pin generator plugin versions in `buf.gen.yaml`.

Servers implementing this contract advertise `schema_revision = 1`, `minimum_client_revision = 1`, and the immutable BSR module commit in `ServerInfo.schema_release`.

## Resources

- [Schema source](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
- [API reference](https://github.com/ai-dynamo/openengine/blob/main/docs/api.md)
- [Motivation and adoption model](https://github.com/ai-dynamo/openengine/blob/main/docs/motivation.md)
- [Release process](https://github.com/ai-dynamo/openengine/blob/main/RELEASING.md)
- [Contributing](https://github.com/ai-dynamo/openengine/blob/main/CONTRIBUTING.md)
- [Security policy](https://github.com/ai-dynamo/openengine/blob/main/SECURITY.md)
- [Apache-2.0 license](https://github.com/ai-dynamo/openengine/blob/main/LICENSE)
