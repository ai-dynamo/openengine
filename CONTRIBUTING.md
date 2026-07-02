<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Contributing to OpenEngine

Thank you for your interest in OpenEngine. We welcome bug reports, feedback on
the API design, and pull requests.

OpenEngine is a pre-adoption API draft. `proto/openengine.proto` is the canonical
wire contract and the single source of truth. Until an external consumer adopts
it, the schema may remove or renumber fields to stay minimal. After external
adoption, changes within `openengine.v1` will be additive. Please open an issue
to discuss protocol changes before sending a PR.

- **Bugs / feedback / design questions**: open a [GitHub issue](https://github.com/ai-dynamo/openengine/issues).
- **Pull requests**: open against `main`. Keep changes focused (one logical change per PR).

## Signing Your Work

We require that all contributors "sign off" on their commits. This certifies that
you wrote the contribution, or otherwise have the right to submit it under the
project's [Apache 2.0 license](LICENSE).

Any contribution containing commits that are not signed off will not be accepted.

To sign off on a commit, use the `--signoff` (or `-s`) option when committing:

```bash
git commit -s -m "Add a concise, descriptive message."
```

This appends the following to your commit message:

```
Signed-off-by: Your Name <your@email.com>
```

Use your real name (no pseudonyms or anonymous contributions) and an email that
matches your commit author address. By signing off, you agree to the Developer
Certificate of Origin (DCO), reproduced in full below.

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

By contributing, you agree that your contributions will be licensed under the
[Apache 2.0 License](LICENSE).
