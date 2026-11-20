<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine v1 schema

This directory is the canonical `openengine.v1` wire contract. All proto files
share the same package and together define the API.

The current contract is schema revision 1 and remains compatible with clients at revision 1. The [OpenEngine v0.1.0 release notes](https://github.com/ai-dynamo/openengine/releases/tag/v0.1.0) record its immutable BSR commit. Published servers advertise that commit in `ServerInfo.schema_release`. Unpublished builds may use a source commit.

| File | Area |
| --- | --- |
| [`openengine.proto`](openengine.proto) | `Inference` and `Control` service declarations |
| [`server.proto`](server.proto) | Server identity, deployment capacity, engine roles, parallelism, and load |
| [`model.proto`](model.proto) | Model metadata and inference capabilities |
| [`generation.proto`](generation.proto) | Generation inputs, requests, parameters, streamed events, and usage |
| [`lora.proto`](lora.proto) | LoRA adapter lifecycle |
| [`kv.proto`](kv.proto) | KV sessions, connector discovery, and cache events |
| [`lifecycle.proto`](lifecycle.proto) | Health and abort operations |
| [`error.proto`](error.proto) | Terminal errors for accepted streaming requests |

Generate bindings from every `.proto` file in this directory. Compiling only
`openengine.proto` does not generate bindings for its imported message files.

The [`openengine` Rust crate](../../../packages/rust/openengine/) targets the published schema identified in its release manifest. The generation entry point is [`scripts/generate-rust.sh`](../../../scripts/generate-rust.sh).
