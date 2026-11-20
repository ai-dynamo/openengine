#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! $1 =~ ^openengine-v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  echo "usage: $0 openengine-vMAJOR.MINOR.PATCH" >&2
  exit 2
fi

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
tag_version=${BASH_REMATCH[1]}
crate_version=$(
  cargo metadata \
    --manifest-path "${repository}/Cargo.toml" \
    --no-deps \
    --format-version 1 \
    | jq --raw-output '.packages[] | select(.name == "openengine") | .version'
)

if [[ -z ${crate_version} || ${crate_version} != "${tag_version}" ]]; then
  echo "release tag: ${tag_version}" >&2
  echo "Rust crate: ${crate_version:-not found}" >&2
  exit 1
fi

echo "OpenEngine crate release version matches: ${tag_version}"
