#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

if [[ -f Cargo.toml ]]; then
  echo "present=true" >> "$GITHUB_OUTPUT"
else
  rust_files=$(git ls-files -- 'Cargo.lock' '**/Cargo.toml' '**/Cargo.lock')
  if [[ -n "$rust_files" ]]; then
    echo "::error::Rust files exist but the workspace Cargo.toml is missing"
    exit 1
  fi
  echo "present=false" >> "$GITHUB_OUTPUT"
  echo "No Rust workspace is present at this commit." >> "$GITHUB_STEP_SUMMARY"
fi
