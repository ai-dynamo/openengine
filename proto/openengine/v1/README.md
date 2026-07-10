<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine v1 schema

This directory is the canonical `openengine.v1` wire contract. All proto files
share the same package and together define the API.

| File | Area |
| --- | --- |
| [`openengine.proto`](openengine.proto) | `OpenEngine` service and RPC declarations |
| [`engine.proto`](engine.proto) | Engine identity, roles, and parallelism |
| [`model.proto`](model.proto) | Model metadata and generation capabilities |
| [`generation.proto`](generation.proto) | Generation requests, streamed events, and usage |
| [`generation_params.proto`](generation_params.proto) | Sampling, stopping, response, KV, and guided-decoding parameters |
| [`lora.proto`](lora.proto) | LoRA adapter lifecycle |
| [`kv.proto`](kv.proto) | KV sessions, connector discovery, and cache events |
| [`lifecycle.proto`](lifecycle.proto) | Health, abort, and drain operations |
| [`observability.proto`](observability.proto) | Load snapshots and runtime events |
| [`error.proto`](error.proto) | Terminal errors for accepted streaming requests |

Generate bindings from every `.proto` file in this directory. Compiling only
`openengine.proto` does not generate bindings for its imported message files.

OpenEngine publishes pre-generated bindings from this package for Python and
Rust. Their sources and package manifests live under [`packages/`](../../../packages/),
and the generation entry points live under [`scripts/`](../../../scripts/).
