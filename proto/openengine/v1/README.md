<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine v1 schema

This directory is the canonical `openengine.v1` wire contract. All proto files
share the same package and together define the API.

| File | Area |
| --- | --- |
| [`openengine.proto`](openengine.proto) | `Inference` and `Control` service declarations |
| [`input.proto`](input.proto) | Shared text, token, and multimodal inputs |
| [`server.proto`](server.proto) | Server identity, deployment capacity, engine roles, and parallelism |
| [`model.proto`](model.proto) | Model metadata and inference capabilities |
| [`generation.proto`](generation.proto) | Generation requests, parameters, streamed events, and usage |
| [`lora.proto`](lora.proto) | LoRA adapter lifecycle |
| [`kv.proto`](kv.proto) | KV sessions, connector discovery, and cache events |
| [`lifecycle.proto`](lifecycle.proto) | Health, abort, and drain operations |
| [`observability.proto`](observability.proto) | Load snapshots |
| [`error.proto`](error.proto) | Terminal errors for accepted streaming requests |

Generate bindings from every `.proto` file in this directory. Compiling only
`openengine.proto` does not generate bindings for its imported message files.
