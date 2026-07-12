#!/usr/bin/env python3
"""Encode or verify the shared Python/Rust wire fixture."""

from __future__ import annotations

import sys
from pathlib import Path

from openengine.v1.generation_pb2 import GenerateRequest
from openengine.v1.input_pb2 import MODALITY_IMAGE, MODALITY_VIDEO, MediaItem


def fixture() -> GenerateRequest:
    return GenerateRequest(
        request_id="cross-language",
        model="test-model",
        prompt="Hello",
        priority=0,
        media=[
            MediaItem(
                modality=MODALITY_IMAGE,
                raw_bytes=b"\x00\x01\xff",
                mime_type="image/png",
                uuid="image-0",
            ),
            MediaItem(
                modality=MODALITY_VIDEO,
                url="https://example.invalid/video.mp4",
                uuid="video-1",
            ),
        ],
        media_options={
            "image": {"min_pixels": 3136, "do_resize": True},
            "video": {"max_frames": 8},
        },
    )


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"encode", "decode"}:
        print("usage: cross_language_fixture.py (encode|decode) PATH", file=sys.stderr)
        return 2

    operation, raw_path = sys.argv[1:]
    path = Path(raw_path)
    if operation == "encode":
        path.write_bytes(fixture().SerializeToString())
        return 0

    decoded = GenerateRequest.FromString(path.read_bytes())
    if decoded != fixture():
        print("decoded Rust fixture does not match the Python fixture", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
