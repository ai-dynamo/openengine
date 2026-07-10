#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
temporary_directory=$(mktemp -d)
python=${PYTHON:-python3}
trap 'rm -rf "${temporary_directory}"' EXIT

export PYTHONPATH="${repository}/packages/python/src${PYTHONPATH:+:${PYTHONPATH}}"

"${python}" "${repository}/scripts/cross_language_fixture.py" \
  encode "${temporary_directory}/python.bin"
cargo run --quiet \
  --manifest-path "${repository}/Cargo.toml" \
  --package openengine-proto \
  --example cross_language_fixture \
  -- decode "${temporary_directory}/python.bin"

cargo run --quiet \
  --manifest-path "${repository}/Cargo.toml" \
  --package openengine-proto \
  --example cross_language_fixture \
  -- encode "${temporary_directory}/rust.bin"
"${python}" "${repository}/scripts/cross_language_fixture.py" \
  decode "${temporary_directory}/rust.bin"
