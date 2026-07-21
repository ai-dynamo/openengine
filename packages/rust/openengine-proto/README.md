<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine Rust bindings

Generated Prost messages and Tonic client/server bindings for the
[`openengine.v1`](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
protocol.

```toml
openengine-proto = { path = "../openengine/packages/rust/openengine-proto" }
```

```rust
use openengine_proto::openengine::v1::{
    inference_client::InferenceClient,
    GenerateRequest,
};
```

The crate contains generated Rust source and a protobuf descriptor set.
Consumer builds do not run `protoc`.

`SCHEMA_RELEASE` is deliberately `"unreleased"`: an engine server must inject
the immutable OpenEngine commit SHA (or signed release tag) used by that build.
The crate version alone is not a source identity for path or Git dependencies.
