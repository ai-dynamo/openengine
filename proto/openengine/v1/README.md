<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine v1 schema

The files in this directory share the `openengine.v1` package and define its API.

The schema on `main` includes `Control.Shutdown`, which was added after v0.1.0. To call it, generate bindings from a commit that defines the RPC. Servers without shutdown support return gRPC `UNIMPLEMENTED`.

Both v0.1.0 and the schema on `main` advertise schema revision `1` and minimum client revision `1`. Before routing traffic using the named `readiness` or `liveness` probes, call `grpc.health.v1.Health/Check` for each name your deployment uses and verify that the engine recognizes it. See the [health status and error rules](../../../docs/api.md#standard-grpc-health).

Set `ServerInfo.schema_release` to the immutable BSR commit used for the server bindings, or the exact source commit for an unpublished build.

The [short request guide](../../../docs/QUICKSTART.md) has text and multimodal examples. The [API reference](../../../docs/api.md) defines each field and its validation rules.

| File | Area |
| --- | --- |
| [`openengine.proto`](openengine.proto) | `Inference` and `Control` service declarations |
| [`server.proto`](server.proto) | Server identity, deployment capacity, engine roles, parallelism, and load |
| [`model.proto`](model.proto) | Model metadata and inference capabilities |
| [`generation.proto`](generation.proto) | Generation inputs, requests, parameters, streamed events, and usage |
| [`lora.proto`](lora.proto) | LoRA adapter lifecycle |
| [`kv.proto`](kv.proto) | KV sessions, connector discovery, and cache events |
| [`lifecycle.proto`](lifecycle.proto) | Detailed health, abort, and shutdown operations |
| [`error.proto`](error.proto) | Terminal errors for accepted streaming requests |

Generate bindings from every `.proto` file in this directory. Compiling only
`openengine.proto` does not generate bindings for its imported message files.
