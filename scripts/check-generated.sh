#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

"${repository}/scripts/generate-python.sh"
"${repository}/scripts/generate-rust.sh"

if [[ -n $(git -C "${repository}" status --porcelain --untracked-files=all -- \
  packages/python/src/openengine/v1 \
  packages/rust/openengine-proto/src/generated) ]]; then
  git -C "${repository}" diff -- \
    packages/python/src/openengine/v1 \
    packages/rust/openengine-proto/src/generated
  git -C "${repository}" status --short -- \
    packages/python/src/openengine/v1 \
    packages/rust/openengine-proto/src/generated
  echo "Generated bindings are out of date. Run the generation scripts and commit the result." >&2
  exit 1
fi
