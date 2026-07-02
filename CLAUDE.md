<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine proto — edit & regen discipline

`proto/openengine.proto` is the **single source of truth** for the OpenEngine
v1 wire contract. Consumer repositories generate stubs from vendored copies.
Treat changes here as changes to a shared public API.

## Hard rules

1. **One canonical proto.** Consumers generate gRPC stubs at build time from a
   vendored copy. Change `proto/openengine.proto`, run `./gen.sh`, and rebuild
   each consumer. Do not edit generated stubs.

2. **Keep `package openengine.v1;` and `syntax = "proto3";` fixed.** The
   package name is part of the gRPC service path
   (`openengine.v1.OpenEngine/Generate`). Changing it breaks every client.

3. **Pre-adoption cleanup is synchronized.** OpenEngine has no external
   consumers yet. An explicitly approved cleanup may remove or renumber fields,
   but every local client, server, test, doc, and vendored proto must update in
   the same change. Do not retain deprecated aliases before adoption.

4. **Additive-only after adoption.** Once an external consumer adopts v1,
   removing or renumbering fields requires a new package.

5. **Enum zero value stays UNSPECIFIED.** Every enum's `0` is the
   `*_UNSPECIFIED` sentinel (proto3 default). Don't assign semantic meaning to
   `0`.

## After editing the proto

Sync the vendored copies, rebuild, and re-run their unit tests:

```bash
./gen.sh
cargo build
```

Then update [`docs/api.md`](docs/api.md). If the reference and proto disagree,
the proto wins.

## Semver

`api_version` in `EngineInfo` is `openengine.v1`. After external adoption, a
breaking change requires a new package and `api_version`.
