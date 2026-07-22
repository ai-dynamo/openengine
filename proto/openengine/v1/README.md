<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine v1 schema

This directory is the canonical `openengine.v1` wire contract. All proto files
share the same package and together define the API.

The current contract is schema revision 3 and remains compatible with clients
at revision 1. Servers built from source advertise the immutable OpenEngine
commit SHA in `ServerInfo.schema_release`.

| File | Area |
| --- | --- |
| [`openengine.proto`](openengine.proto) | `Inference` and `Control` service declarations |
| [`input.proto`](input.proto) | Shared text, token, and multimodal inputs |
| [`server.proto`](server.proto) | Server identity, deployment capacity, engine roles, and parallelism |
| [`model.proto`](model.proto) | Model metadata and inference capabilities |
| [`generation.proto`](generation.proto) | Generation requests, parameters, streamed events, and usage |
| [`tasks.proto`](tasks.proto) | Reserved non-generative task request and output vocabulary |
| [`embedding.proto`](embedding.proto) | Reserved dense and sparse embedding messages |
| [`classification.proto`](classification.proto) | Reserved sequence and token classification messages |
| [`scoring.proto`](scoring.proto) | Reserved grouped query and candidate scoring messages |
| [`lora.proto`](lora.proto) | LoRA adapter lifecycle |
| [`kv.proto`](kv.proto) | KV sessions, connector discovery, and cache events |
| [`lifecycle.proto`](lifecycle.proto) | Health, abort, and drain operations |
| [`observability.proto`](observability.proto) | Load snapshots and reserved runtime-event messages |
| [`error.proto`](error.proto) | Terminal errors for accepted streaming requests |

Generate bindings from every `.proto` file in this directory. Compiling only
`openengine.proto` does not generate bindings for its imported message files.

OpenEngine provides pre-generated bindings from this package for Python and
Rust. Their sources and package manifests live under [`packages/`](../../../packages/),
and the generation entry points live under [`scripts/`](../../../scripts/).
