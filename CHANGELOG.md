<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

All notable changes to the OpenEngine schema are documented here. Published
schema releases are immutable commits in the Buf Schema Registry.

## [Unreleased]

### Added

- Initial revision-1 `openengine.v1` inference and control services.
- Aggregate and context-first prefill/decode generation.
- Health, abort, drain, load, LoRA, and KV-event control operations.
- Active tokenizer discovery and multimodal routing-token metadata.
- Named KV handoff profiles and typed client bootstrap rendezvous metadata.
- Canonical schema revision values in `version.proto`.

### Changed

- Consolidated generation inputs into `generation.proto` and load reporting into `server.proto`.
- Made the BSR module the sole schema distribution mechanism.

### Removed

- Unimplemented embedding, classification, scoring, and runtime-event subscription RPCs.
- Dedicated KV-connector discovery RPC; connector metadata is reported by `GetServerInfo`.

[Unreleased]: https://github.com/ai-dynamo/openengine/commits/main
