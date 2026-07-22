#!/usr/bin/env python3
"""Encode or verify the shared Python/Rust wire fixture."""

from __future__ import annotations

import sys
from pathlib import Path

from openengine.v1.generation_pb2 import GenerateRequest
from openengine.v1.input_pb2 import MODALITY_IMAGE, MODALITY_VIDEO, MediaItem
from openengine.v1.kv_pb2 import KvBootstrap, KvEndpoint, KvSessionRef


HANDOFF_PROFILES = (
    "tensorrt_llm.disaggregated_params.v1",
    "vllm.kv_transfer_params.v1",
    "sglang.bootstrap.v1",
)
LARGE_IDENTIFIER = "18446744073709551614"
ROOM_ID = 18446744073709551614


def kv_session(profile: str) -> KvSessionRef:
    endpoint = KvEndpoint(host="decode.internal", port=24000, protocol="tcp")
    if profile == HANDOFF_PROFILES[0]:
        attributes = {
            profile: (
                '{"ctx_request_id":"18446744073709551614",'
                '"opaque_state":"AP8="}'
            )
        }
    elif profile == HANDOFF_PROFILES[1]:
        attributes = {
            "request_id": LARGE_IDENTIFIER,
            "opaque_state": "AP8=",
        }
    elif profile == HANDOFF_PROFILES[2]:
        attributes = {
            "bootstrap_owner": "client",
            "opaque_state": "AP8=",
        }
    else:
        raise ValueError(f"unknown handoff profile: {profile}")

    session = KvSessionRef(
        session_id="cross-language-session",
        transfer_backend="fixture",
        endpoints=[endpoint],
        dp_rank=7,
        attributes_struct=attributes,
        handoff_profile=profile,
    )
    if profile == "sglang.bootstrap.v1":
        session.bootstrap.CopyFrom(KvBootstrap(endpoint=endpoint, room_id=ROOM_ID))
    return session


def fixture(profile: str) -> GenerateRequest:
    return GenerateRequest(
        request_id="cross-language",
        model="test-model",
        prompt="Hello",
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
        kv={"session": kv_session(profile)},
    )


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"encode", "decode"}:
        print(
            "usage: cross_language_fixture.py (encode|decode) PROFILE PATH",
            file=sys.stderr,
        )
        return 2

    operation, profile, raw_path = sys.argv[1:]
    if profile not in HANDOFF_PROFILES:
        print(f"unknown handoff profile: {profile}", file=sys.stderr)
        return 2
    path = Path(raw_path)
    if operation == "encode":
        path.write_bytes(fixture(profile).SerializeToString())
        return 0

    decoded = GenerateRequest.FromString(path.read_bytes())
    if decoded != fixture(profile):
        print("decoded Rust fixture does not match the Python fixture", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
