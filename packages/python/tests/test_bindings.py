import unittest

import grpc

from openengine import (
    MINIMUM_CLIENT_REVISION,
    SCHEMA_RELEASE,
    SCHEMA_REVISION,
)
from openengine.v1.generation_pb2 import GenerateRequest
from openengine.v1.input_pb2 import (
    MEDIA_SOURCE_TYPE_DATA_URI,
    MEDIA_SOURCE_TYPE_RAW_BYTES,
    MEDIA_SOURCE_TYPE_URL,
    MODALITY_AUDIO,
    MODALITY_IMAGE,
    MODALITY_VIDEO,
)
from openengine.v1.kv_pb2 import KvBootstrap, KvConnectorInfo, KvSessionRef
from openengine.v1.model_pb2 import ModelInfo, MultimodalCapabilities
from openengine.v1.openengine_pb2_grpc import ControlStub, InferenceStub


class BindingsTest(unittest.TestCase):
    def test_request_round_trip_preserves_optional_zero(self) -> None:
        request = GenerateRequest(
            request_id="python-smoke",
            model="test-model",
            prompt="Hello",
            sampling={"temperature": 0.0},
        )

        decoded = GenerateRequest.FromString(request.SerializeToString())

        self.assertEqual(decoded.request_id, "python-smoke")
        self.assertEqual(decoded.WhichOneof("input"), "prompt")
        self.assertTrue(decoded.sampling.HasField("temperature"))
        self.assertEqual(decoded.sampling.temperature, 0.0)

    def test_multimodal_contract_round_trip(self) -> None:
        request = GenerateRequest(
            request_id="multimodal",
            model="test-model",
            prompt="<image><video><audio>",
            media=[
                {"modality": MODALITY_IMAGE, "raw_bytes": b"\x00\xff"},
                {
                    "modality": MODALITY_VIDEO,
                    "url": "https://example.invalid/video.mp4",
                },
                {
                    "modality": MODALITY_AUDIO,
                    "data_uri": "data:audio/wav;base64,AA==",
                },
            ],
            media_options={"image": {"min_pixels": 3136}},
        )

        decoded = GenerateRequest.FromString(request.SerializeToString())

        self.assertEqual([item.modality for item in decoded.media], [1, 2, 3])
        self.assertEqual(decoded.media[0].raw_bytes, b"\x00\xff")
        self.assertEqual(decoded.media_options["image"]["min_pixels"], 3136)

    def test_multimodal_capabilities_preserve_optional_false(self) -> None:
        info = ModelInfo(
            model_id="test-model",
            supports_multimodal=True,
            multimodal_capabilities=MultimodalCapabilities(
                aggregate_modalities=[MODALITY_IMAGE, MODALITY_VIDEO, MODALITY_AUDIO],
                prefill_decode_modalities=[MODALITY_IMAGE, MODALITY_VIDEO],
                source_types=[
                    MEDIA_SOURCE_TYPE_URL,
                    MEDIA_SOURCE_TYPE_DATA_URI,
                    MEDIA_SOURCE_TYPE_RAW_BYTES,
                ],
                supports_per_request_media_options=False,
            ),
        )

        decoded = ModelInfo.FromString(info.SerializeToString())

        self.assertTrue(decoded.supports_multimodal)
        self.assertTrue(
            decoded.multimodal_capabilities.HasField(
                "supports_per_request_media_options"
            )
        )
        self.assertFalse(
            decoded.multimodal_capabilities.supports_per_request_media_options
        )

    def test_revision_2_field_numbers_are_stable(self) -> None:
        self.assertEqual(
            GenerateRequest.DESCRIPTOR.fields_by_name["media_options"].number, 14
        )
        self.assertEqual(
            ModelInfo.DESCRIPTOR.fields_by_name["multimodal_capabilities"].number,
            29,
        )

    def test_revision_3_field_numbers_are_stable(self) -> None:
        self.assertEqual(ModelInfo.DESCRIPTOR.fields_by_name["tokenizer"].number, 11)
        self.assertEqual(
            MultimodalCapabilities.DESCRIPTOR.fields_by_name[
                "routing_image_token_id"
            ].number,
            5,
        )
        self.assertEqual(
            KvSessionRef.DESCRIPTOR.fields_by_name["handoff_profile"].number, 6
        )
        self.assertEqual(
            KvSessionRef.DESCRIPTOR.fields_by_name["bootstrap"].number, 7
        )
        self.assertEqual(
            KvBootstrap.DESCRIPTOR.fields_by_name["endpoint"].number, 1
        )
        self.assertEqual(
            KvBootstrap.DESCRIPTOR.fields_by_name["room_id"].number, 2
        )
        self.assertEqual(
            KvConnectorInfo.DESCRIPTOR.fields_by_name["handoff_profile"].number,
            10,
        )
        self.assertEqual(
            KvConnectorInfo.DESCRIPTOR.fields_by_name[
                "supports_client_bootstrap"
            ].number,
            11,
        )

    def test_client_stub_can_be_constructed(self) -> None:
        channel = grpc.insecure_channel("localhost:1")
        self.addCleanup(channel.close)

        inference = InferenceStub(channel)
        control = ControlStub(channel)

        self.assertTrue(callable(inference.Generate))
        self.assertTrue(callable(control.GetServerInfo))

    def test_package_metadata_matches_schema(self) -> None:
        self.assertEqual(SCHEMA_REVISION, 3)
        self.assertEqual(MINIMUM_CLIENT_REVISION, 1)
        self.assertEqual(SCHEMA_RELEASE, "unreleased")


if __name__ == "__main__":
    unittest.main()
