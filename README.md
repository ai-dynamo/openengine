<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

<p align="center">
  <img src="docs/assets/logo.png" alt="OpenEngine" width="320">
</p>

OpenEngine is a vendor-neutral gRPC protocol between inference engines and
orchestrators. Engines serve `openengine.v1`; orchestrators call it.

> **Experimental and exploratory.** OpenEngine is an attempt to standardize this
> boundary, not a finalized standard. It is one direction we are exploring for how
> inference orchestrators integrate with inference engines, and it may change
> substantially before its final implementation.

## Documentation

| Document | Purpose |
|---|---|
| [Why OpenEngine](docs/motivation.md) | Boundary, tradeoffs, and adoption path |
| [API reference](docs/api.md) | Human-readable `openengine.v1` reference |
| [Canonical proto](proto/openengine.proto) | Wire contract and source of truth |

## Status

OpenEngine is a pre-adoption API draft. Until an external consumer adopts it, the
contract may remove or renumber fields to keep the schema clean.

The current wire contract is schema revision `1`. Servers advertise their exact
revision, minimum compatible client revision, and immutable schema release/tag
through `GetEngineInfo`.

After external adoption, changes within `openengine.v1` are additive:

- Existing field numbers, names, and types do not change.
- Enum value `0` remains the `*_UNSPECIFIED` sentinel.
- Breaking changes require a new package such as `openengine.v2`.

## API surface

| Area | RPCs |
|---|---|
| Generation | `Generate` |
| Metadata | `GetEngineInfo`, `GetModelInfo`, `GetLoad` |
| Lifecycle | `Health`, `Abort`, `Drain` |
| LoRA lifecycle | `LoadLora`, `UnloadLora`, `ListLoras` |
| KV and disaggregation | `GetKvConnectorInfo`, `GetKvEventSources`, `SubscribeKvEvents` |
| Runtime events | `SubscribeRuntimeEvents` |

## Generate Code

Use a proto3 toolchain with explicit-optional support (`protoc` 3.15 or newer).
Include the protobuf well-known types because the contract imports
`google/protobuf/struct.proto`.

```bash
PROTO_INCLUDE=$(python -c \
  'import grpc_tools, os; print(os.path.join(os.path.dirname(grpc_tools.__file__), "_proto"))')
python -m grpc_tools.protoc \
  -I proto \
  -I "$PROTO_INCLUDE" \
  --python_out=. \
  --grpc_python_out=. \
  proto/openengine.proto
```

## Validate the schema

Install [Buf](https://buf.build/docs/cli/installation/) and run:

```bash
buf lint
buf breaking --against '.git#branch=main,subdir=proto'
```

CI runs lint for schema changes on `main` and pull requests. Pull requests also
run the `FILE` breaking-change policy against their base commit.
