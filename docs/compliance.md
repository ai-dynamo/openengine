<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Compliance checks

The `Compliance` workflow contains two independently required jobs: `SPDX headers` checks tracked-file attribution, and `Cargo deny` checks the full Rust workspace dependency graph, including transitive dependencies and the unpublished generator. Both jobs report on every PR, pushes to `main`, and merge groups; there are no path filters. Branch protection requires these check names from the GitHub Actions app, alongside the existing DCO requirement. The workflow name is descriptive; the job check names are the merge requirements.

## Dependency policy

`deny.toml` allows MIT, BSD-2-Clause, BSD-3-Clause, ISC, Zlib, and Apache-2.0. Unknown or unapproved licenses fail. One exact crate/version exception allows Unicode-3.0 for `unicode-ident =1.0.24`, whose license is `(MIT OR Apache-2.0) AND Unicode-3.0`. This does not allow Unicode-3.0 for other crates or versions. Reassess the exception when updating that dependency.

The job also checks known security advisories, dependency bans, and sources. Multiple versions produce warnings; wildcard dependency requirements and unknown Git or registry sources fail. No security advisory is ignored by this policy. A license exception does not waive vulnerability findings.

Run the same checks locally with cargo-deny 0.19.4:

```bash
cargo deny --locked --all-features check licenses advisories bans sources
```

The job uses Rust 1.98.1 and cargo-deny 0.19.4. Before the Rust bindings workspace lands, it reports success with a summary explaining that no Rust workspace is present. A nested Cargo manifest or lockfile without the root workspace manifest fails. Once the root `Cargo.toml` exists, the dependency checks run on every invocation.

## Policy ownership

`/deny.toml` is owned exclusively by `@ai-dynamo/dynamo-function-compliance` in CODEOWNERS. With required code-owner reviews enabled on `main`, future changes to the dependency policy or license exceptions require approval from that team. GitHub evaluates ownership from the PR base branch, so this new ownership rule takes effect after this PR merges.

## SPDX attribution

See [SPDX headers](spdx.md) for supported source headers, generated files, reviewed sidecars, and third-party attribution. These automated checks do not replace release approval.
