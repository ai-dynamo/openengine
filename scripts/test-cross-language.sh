#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
temporary_directory=$(mktemp -d)
python=${PYTHON:-python3}
trap 'rm -rf "${temporary_directory}"' EXIT

export PYTHONPATH="${repository}/packages/python/src${PYTHONPATH:+:${PYTHONPATH}}"

for profile in \
  tensorrt_llm.disaggregated_params.v1 \
  vllm.kv_transfer_params.v1 \
  sglang.bootstrap.v1; do
  fixture_name=${profile//./_}

  "${python}" "${repository}/scripts/cross_language_fixture.py" \
    encode "${profile}" "${temporary_directory}/python-${fixture_name}.bin"
  cargo run --quiet \
    --manifest-path "${repository}/Cargo.toml" \
    --package openengine-proto \
    --example cross_language_fixture \
    -- decode "${profile}" "${temporary_directory}/python-${fixture_name}.bin"

  cargo run --quiet \
    --manifest-path "${repository}/Cargo.toml" \
    --package openengine-proto \
    --example cross_language_fixture \
    -- encode "${profile}" "${temporary_directory}/rust-${fixture_name}.bin"
  "${python}" "${repository}/scripts/cross_language_fixture.py" \
    decode "${profile}" "${temporary_directory}/rust-${fixture_name}.bin"
done
