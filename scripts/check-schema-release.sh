#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

if (( $# > 1 )); then
  echo "usage: $0 [--verify-registry]" >&2
  exit 2
fi
if (( $# == 1 )) && [[ $1 != "--verify-registry" ]]; then
  echo "usage: $0 [--verify-registry]" >&2
  exit 2
fi

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
manifest="${repository}/packages/rust/openengine/schema-release.json"

crate_version=$(jq --exit-status --raw-output '.crate_version' "${manifest}")
schema_revision=$(jq --exit-status --raw-output '.schema_revision' "${manifest}")
schema_release=$(jq --exit-status --raw-output '.schema_release' "${manifest}")
schema_tag=$(jq --exit-status --raw-output '.schema_git_tag' "${manifest}")
schema_commit=$(jq --exit-status --raw-output '.schema_git_commit' "${manifest}")

workspace_version=$(
  cargo metadata \
    --manifest-path "${repository}/Cargo.toml" \
    --no-deps \
    --format-version 1 \
    | jq --raw-output '.packages[] | select(.name == "openengine") | .version'
)

if [[ -z ${workspace_version} || ${workspace_version} != "${crate_version}" ]]; then
  echo "schema release manifest: ${crate_version}" >&2
  echo "Rust crate: ${workspace_version:-not found}" >&2
  exit 1
fi

if ! git -C "${repository}" cat-file -e "${schema_commit}^{commit}"; then
  echo "Schema Git commit is unavailable: ${schema_commit}" >&2
  echo "Fetch the repository history and tags before running this check." >&2
  exit 1
fi

if ! tag_object=$(git -C "${repository}" show-ref --verify --hash "refs/tags/${schema_tag}"); then
  echo "Schema Git tag not found: ${schema_tag}. Fetch the schema release tag." >&2
  exit 1
fi
tag_commit=$(git -C "${repository}" rev-parse --verify "${tag_object}^{commit}")
if [[ ${tag_commit} != "${schema_commit}" ]]; then
  echo "Schema Git tag ${schema_tag}: ${tag_commit}" >&2
  echo "Schema Git commit: ${schema_commit}" >&2
  exit 1
fi

check_revision() {
  local source=$1 declaration
  if ! declaration=$(grep -oE '`schema_revision = [0-9]+`') ||
     [[ ${declaration} != "\`schema_revision = ${schema_revision}\`" ]]; then
    echo "Expected schema revision ${schema_revision} in ${source}. Found: ${declaration:-no declaration}" >&2
    return 1
  fi
}

git -C "${repository}" show "${schema_commit}:proto/buf.md" | check_revision "${schema_tag}:proto/buf.md"

if [[ ${1:-} == "--verify-registry" ]]; then
  archive=$(mktemp)
  local_protos="${archive}.local"
  published_protos="${archive}.published"
  trap 'rm -f "${archive}" "${local_protos}" "${published_protos}"' EXIT
  curl \
    --silent \
    --show-error \
    --fail \
    --retry 3 \
    "https://buf.build/openengine/openengine/archive/${schema_release}.tar.gz" \
    --output "${archive}"

  tar -xOzf "${archive}" buf.md | check_revision "BSR commit ${schema_release}"

  git -C "${repository}" ls-tree -r --name-only "${schema_commit}:proto" \
    | sed -n '/\.proto$/p' \
    | sort \
    > "${local_protos}"
  tar -tzf "${archive}" \
    | sed -n '/\.proto$/p' \
    | sort \
    > "${published_protos}"

  if [[ ! -s ${local_protos} ]] || ! cmp -s "${local_protos}" "${published_protos}"; then
    echo "Local proto files:" >&2
    cat "${local_protos}" >&2
    echo "Published proto files:" >&2
    cat "${published_protos}" >&2
    exit 1
  fi

  while IFS= read -r proto; do
    published_blob=$(tar -xOzf "${archive}" "${proto}" | git -C "${repository}" hash-object --stdin)
    pinned_blob=$(git -C "${repository}" rev-parse "${schema_commit}:proto/${proto}")
    if [[ ${published_blob} != "${pinned_blob}" ]]; then
      echo "Published schema differs from the packaged schema: ${proto}" >&2
      exit 1
    fi
  done < "${local_protos}"
fi

echo "OpenEngine crate metadata matches ${schema_tag} (${schema_commit})."
