<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Compliance checks

The `Compliance` workflow contains two independently required jobs: `SPDX headers` checks tracked-file attribution, and `Cargo deny` checks the full Rust workspace dependency graph, including transitive dependencies and the unpublished generator. A separate, non-required `Rust CVE audit` job uses cargo-audit to report High and Critical vulnerabilities. All three jobs report on every PR, pushes to `main` and `release/*` branches, and merge groups; there are no path filters. Branch protection requires these check names from the GitHub Actions app, alongside the existing DCO requirement. The workflow name is descriptive; the job check names are the merge requirements.

## Dependency policy

`deny.toml` allows MIT, BSD-2-Clause, BSD-3-Clause, ISC, Zlib, and Apache-2.0. Unknown or unapproved licenses fail. One exact crate/version exception allows Unicode-3.0 for `unicode-ident =1.0.24`, whose license is `(MIT OR Apache-2.0) AND Unicode-3.0`. This does not allow Unicode-3.0 for other crates or versions. Reassess the exception when updating that dependency.

The job also checks dependency bans and sources. Multiple versions produce warnings; wildcard dependency requirements and unknown Git or registry sources fail. Vulnerability scanning is handled separately by cargo-audit; the cargo-deny invocation intentionally omits the advisories check. No per-advisory ignore list is added.

Run the same checks locally with cargo-deny 0.19.4:

```bash
cargo deny --locked --all-features check licenses bans sources
```

The job uses Rust 1.98.1 and cargo-deny 0.19.4. Before the Rust bindings workspace lands, it reports success with a summary explaining that no Rust workspace is present. A nested Cargo manifest or lockfile without the root workspace manifest fails. Once the root `Cargo.toml` exists, the dependency checks run on every invocation.

## High and Critical vulnerability report

`Rust CVE audit` uses cargo-audit 0.23.0 with `severity_threshold = "high"` in `.cargo/audit.toml`. It scans `Cargo.lock` using the RustSec advisory database. High and Critical findings fail the job visibly, but this job is not a required merge check. It does not modify manifests or the lockfile, and it uses the same no-workspace detection as cargo-deny.

```bash
cargo audit --file Cargo.lock
```

The required cargo-deny job checks licenses, bans, and sources only. Vulnerability findings are reported by this separate, non-required audit job, so a High or Critical finding does not by itself block a merge. This permits review of findings that have no available patch. The threshold filters only advisories with an explicit CVSS score below High; unscored vulnerability advisories remain reportable. Informational warnings are displayed without failing the job by default.

## Policy ownership

`/deny.toml` is owned exclusively by `@ai-dynamo/dynamo-function-compliance` in CODEOWNERS. With required code-owner reviews enabled on `main`, future changes to the dependency policy or license exceptions require approval from that team. GitHub evaluates ownership from the PR base branch, so this new ownership rule takes effect after this PR merges.

## SPDX attribution

See [SPDX headers](spdx.md) for supported source headers, generated files, reviewed sidecars, and third-party attribution. These automated checks do not replace release approval.
