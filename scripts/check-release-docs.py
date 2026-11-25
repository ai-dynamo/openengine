# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Check documented schema pins against the corresponding GitHub releases."""

import json
import os
import re
from functools import cache
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@cache
def published_commit(tag):
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise SystemExit(f"Invalid schema release tag: {tag}")
    request = Request(f"https://api.github.com/repos/ai-dynamo/openengine/releases/tags/{tag}")
    if token := os.environ.get("GH_TOKEN"):
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(request, timeout=20) as response:
            release = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise
    if release["draft"]:
        return None
    pins = re.findall(
        r"\bImmutable BSR commit\b[ \t:*|]*`([0-9a-f]{32}|[0-9a-f]{40})`",
        release["body"],
        re.IGNORECASE,
    )
    if len(pins) != 1:
        raise SystemExit(f"{tag}: expected one immutable BSR commit in the release notes")
    return pins[0]


def check_pin(source, tag, pin, *, preparing=False):
    expected = published_commit(tag)
    if expected is None:
        if preparing and pin == "pending":
            return
        raise SystemExit(f"{source}: no published GitHub release for {tag}")
    if pin != expected:
        raise SystemExit(f"{source}: found {pin} for {tag}, expected {expected}")


def table_value(readme, field):
    values = re.findall(rf"(?m)^\| {re.escape(field)} \| \[?`([^`]+)`", readme)
    if len(values) != 1:
        raise SystemExit(f"README.md: expected one {field!r} row in the release table")
    return values[0]


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text()
    pin = table_value(readme, "Immutable BSR commit")
    check_pin("README.md", table_value(readme, "Git tag"), pin, preparing=True)
    example_pins = re.findall(r"(?m)^buf generate buf\.build/openengine/openengine:(\S+)\s*$", readme)
    expected_example = "${OPENENGINE_BSR_COMMIT}" if pin == "pending" else pin
    if example_pins != [expected_example]:
        raise SystemExit(f"README.md: the Buf example must use {expected_example}")

    crate = root / "packages/rust/openengine"
    manifest = json.loads((crate / "schema-release.json").read_text())
    tag = manifest["schema_git_tag"]
    check_pin("schema-release.json", tag, manifest["schema_release"])
    schema_link = f"](https://github.com/ai-dynamo/openengine/tree/{tag}/proto/openengine/v1)"
    if schema_link not in (crate / "README.md").read_text():
        raise SystemExit(f"Crate README.md: expected a schema link for {tag}")
