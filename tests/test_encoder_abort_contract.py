# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Wire compatibility for encoder capabilities and reference cleanup."""

import tempfile
import unittest
from pathlib import Path

import grpc_tools
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from grpc_tools import protoc


class EncoderAbortContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "schema.pb"
            result = protoc.main(
                [
                    "protoc",
                    f"-I{root / 'proto'}",
                    f"-I{Path(grpc_tools.__file__).parent / '_proto'}",
                    f"--descriptor_set_out={output}",
                    "--include_imports",
                    str(root / "proto/openengine/v1/openengine.proto"),
                ]
            )
            if result:
                raise RuntimeError("Could not compile the lifecycle contract")
            descriptors = descriptor_pb2.FileDescriptorSet.FromString(
                output.read_bytes()
            )
        pool = descriptor_pool.DescriptorPool()
        for descriptor in descriptors.file:
            pool.Add(descriptor)
        cls.request = message_factory.GetMessageClass(
            pool.FindMessageTypeByName("openengine.v1.AbortRequest")
        )
        cls.capabilities = message_factory.GetMessageClass(
            pool.FindMessageTypeByName("openengine.v1.EncoderCapabilities")
        )
        cls.control = pool.FindServiceByName("openengine.v1.Control")

    def test_existing_targets_and_encoder_reference_roundtrip(self):
        fields = self.request.DESCRIPTOR.fields_by_name
        self.assertEqual(
            {name: field.number for name, field in fields.items()},
            {"request_id": 1, "kv_session": 2, "all_requests": 3, "encoder_cache": 4},
        )
        for name, value in (
            ("request_id", "request"),
            ("kv_session", {"session_id": "session"}),
            ("all_requests", {}),
            ("encoder_cache", {"transfer_backend": "test", "opaque_state": b"opaque"}),
        ):
            with self.subTest(target=name):
                request = self.request(**{name: value})
                decoded = self.request.FromString(request.SerializeToString())
                self.assertEqual(decoded, request)
                self.assertEqual(decoded.WhichOneof("target"), name)
        self.assertEqual(
            fields["encoder_cache"].message_type.full_name,
            "openengine.v1.EncoderCacheRef",
        )
        request.encoder_cache.SetInParent()
        request.request_id = "replacement"
        self.assertFalse(request.HasField("encoder_cache"))

    def test_typed_capabilities_preserve_tags_and_default_to_false(self):
        fields = self.capabilities.DESCRIPTOR.fields_by_name
        self.assertEqual(
            {name: field.number for name, field in fields.items()},
            {
                "schema_version": 1,
                "encoder_only": 2,
                "accepts_cache": 3,
                "transfer_backends": 4,
                "supports_abort_cleanup": 5,
                "requires_cache": 6,
            },
        )
        for name in ("supports_abort_cleanup", "requires_cache"):
            self.assertEqual(fields[name].type, descriptor_pb2.FieldDescriptorProto.TYPE_BOOL)
            self.assertFalse(getattr(self.capabilities(), name))
        for values in (
            {"encoder_only": True, "supports_abort_cleanup": True},
            {"accepts_cache": True, "requires_cache": True},
        ):
            message = self.capabilities(schema_version=1, **values)
            self.assertEqual(
                self.capabilities.FromString(message.SerializeToString()), message
            )

    def test_backend_transfer_is_outside_portable_control(self):
        self.assertNotIn("TransferEncoderCache", self.control.methods_by_name)
        self.assertIn("Abort", self.control.methods_by_name)


if __name__ == "__main__":
    unittest.main()
