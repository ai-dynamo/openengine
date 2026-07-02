#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Sync the canonical openengine.proto into each fork's Rust proto dir. The
# forks generate gRPC stubs at *build time* from their vendored copy via
# tonic-build (Dynamo: `tonic_build`, vLLM: `tonic_prost_build`) — there are no
# committed generated stubs. This script just keeps the vendored copies in
# lockstep with the single source of truth, `proto/openengine.proto`.
#
# Forks are cloned independently (CI/containers), so a cross-fork relative path
# would not resolve — hence each consumer vendors a copy of the proto (a source
# file, committed) and compiles it locally.
#
# Usage:
#   ./gen.sh                 # sync into both sibling forks (default)
#   ./gen.sh <dest.proto>... # sync into explicit destination file paths
#
# Re-run after any edit to proto/openengine.proto, then rebuild both forks so
# tonic regenerates the stubs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTO_FILE="${SCRIPT_DIR}/proto/openengine.proto"

if [[ ! -f "${PROTO_FILE}" ]]; then
  echo "error: canonical proto not found at ${PROTO_FILE}" >&2
  exit 1
fi

# Default consumers: the vLLM and SGLang engine Rust server crates and their
# respective Dynamo sidecar crates.
if [[ $# -gt 0 ]]; then
  DESTS=("$@")
else
  DESTS=(
    "${SCRIPT_DIR}/../vllm/rust/proto/openengine.proto"
    "${SCRIPT_DIR}/../dynamo/lib/vllm-sidecar/proto/openengine.proto"
    "${SCRIPT_DIR}/../sglang/rust/sglang-grpc/proto/openengine.proto"
    "${SCRIPT_DIR}/../dynamo-sglang/lib/sglang-sidecar/proto/openengine.proto"
  )
fi

for dest in "${DESTS[@]}"; do
  mkdir -p "$(dirname "${dest}")"
  cp "${PROTO_FILE}" "${dest}"
  echo "synced -> ${dest}"
done
