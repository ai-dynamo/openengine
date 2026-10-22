#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

cargo run \
  --locked \
  --manifest-path "${repository}/Cargo.toml" \
  --package openengine-rust-codegen \
  -- "${repository}"
