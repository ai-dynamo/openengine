<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine Python bindings

Generated protobuf messages and gRPC client/server bindings for the
[`openengine.v1`](https://github.com/ai-dynamo/openengine/tree/main/proto/openengine/v1)
protocol.

```bash
pip install ./packages/python
```

```python
import grpc

from openengine.v1.generation_pb2 import GenerateRequest
from openengine.v1.openengine_pb2_grpc import InferenceStub

channel = grpc.aio.insecure_channel("localhost:50051")
engine = InferenceStub(channel)
request = GenerateRequest(request_id="example", model="model", prompt="Hello")
```

The package contains generated code. Applications do not need Buf, `protoc`,
or `grpcio-tools`.

`SCHEMA_RELEASE` is deliberately `"unreleased"`: an engine server must inject
the immutable OpenEngine commit SHA (or signed release tag) used by that build.
The package version alone is not a source identity for path or Git dependencies.
