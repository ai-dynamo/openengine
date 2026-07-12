#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
temporary_directory=$(mktemp -d)
trap 'rm -rf "${temporary_directory}"' EXIT

mkdir -p "${temporary_directory}/python" "${temporary_directory}/rust"
cp -a "${repository}/packages/python/src/openengine/v1/." \
  "${temporary_directory}/python/"
cp -a "${repository}/packages/rust/openengine-proto/src/generated/." \
  "${temporary_directory}/rust/"

"${repository}/scripts/generate-python.sh"
"${repository}/scripts/generate-rust.sh"

if ! diff --recursive --unified --new-file \
  "${temporary_directory}/python" \
  "${repository}/packages/python/src/openengine/v1"; then
  echo "Generated Python bindings are out of date." >&2
  exit 1
fi

if ! diff --recursive --unified --new-file \
  "${temporary_directory}/rust" \
  "${repository}/packages/rust/openengine-proto/src/generated"; then
  echo "Generated Rust bindings are out of date." >&2
  exit 1
fi
