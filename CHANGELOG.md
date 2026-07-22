<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

All notable changes to the OpenEngine schema and generated packages are
documented here. OpenEngine uses the same version for its Git tag, Python
distribution, and Rust crate.

## [Unreleased]

## 0.3.0 - 2026-07-21

### Added

- Active tokenizer discovery and multimodal routing-token metadata.
- Named KV handoff profiles and typed client bootstrap rendezvous metadata.

### Removed

- Unimplemented embedding, classification, scoring, and runtime-event subscription RPCs.

## 0.2.0 - 2026-07-12

### Added

- Generated Python protobuf and gRPC bindings.
- Generated Rust Prost and Tonic client/server bindings.
- Reproducible code generation, package CI, and tag-driven releases.
- Revision-2 multimodal capability discovery and per-request media options.

[Unreleased]: https://github.com/ai-dynamo/openengine/commits/main
