<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine Rust bindings

Generated Prost messages and Tonic client/server bindings for the
[`openengine.v1`](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
protocol.

```bash
cargo add openengine
```

```rust
use openengine::v1::{control_client::ControlClient, inference_client::InferenceClient};
```

The crate contains generated Rust source and a protobuf descriptor set.
Consumer builds do not run `protoc`.
