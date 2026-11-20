#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

manifest="${repository}/packages/rust/openengine/schema-release.json"
schema_commit=$(jq -er '.schema_git_commit | select(test("^[0-9a-f]{40}$"))' "${manifest}")
proto_root=$(mktemp -d)
trap 'rm -rf "${proto_root}"' EXIT
git -C "${repository}" archive "${schema_commit}:proto" | tar -x -C "${proto_root}"

cargo run \
  --locked \
  --manifest-path "${repository}/Cargo.toml" \
  --package openengine-rust-codegen \
  -- "${repository}" "${proto_root}"
