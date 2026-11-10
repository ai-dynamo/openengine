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
        cls.kv_connector = message_factory.GetMessageClass(
            pool.FindMessageTypeByName("openengine.v1.KvConnectorInfo")
        )
        cls.options = message_factory.GetMessageClass(
            pool.FindMessageTypeByName("openengine.v1.EncoderOptions")
        )
        cls.control = pool.FindServiceByName("openengine.v1.Control")

    def test_existing_targets_and_encoder_reference_roundtrip(self):
        fields = self.request.DESCRIPTOR.fields_by_name
        self.assertEqual(
            {name: field.number for name, field in fields.items()},
            {"request_id": 1, "kv_session": 2, "all_requests": 3, "encoder_handoff": 4},
        )
        for name, value in (
            ("request_id", "request"),
            ("kv_session", {"session_id": "session"}),
            ("all_requests", {}),
            ("encoder_handoff", {"transfer_backend": "test", "opaque_state": b"opaque"}),
        ):
            with self.subTest(target=name):
                request = self.request(**{name: value})
                decoded = self.request.FromString(request.SerializeToString())
                self.assertEqual(decoded, request)
                self.assertEqual(decoded.WhichOneof("target"), name)
        self.assertEqual(
            fields["encoder_handoff"].message_type.full_name,
            "openengine.v1.EncoderHandoffRef",
        )
        request.encoder_handoff.SetInParent()
        request.request_id = "replacement"
        self.assertFalse(request.HasField("encoder_handoff"))

    def test_discovery_preserves_absent_and_explicit_defaults(self):
        fields = self.capabilities.DESCRIPTOR.fields_by_name
        self.assertEqual(
            {name: field.number for name, field in fields.items()},
            {
                "schema_version": 1,
                "encoder_only": 2,
                "accepts_handoff": 3,
                "supported_transfer_backends": 4,
                "supports_abort_cleanup": 5,
                "requires_handoff": 6,
                "transfer_backend": 7,
            },
        )
        for name, value in (
            ("schema_version", 0),
            ("encoder_only", False),
            ("accepts_handoff", False),
            ("supports_abort_cleanup", False),
            ("requires_handoff", False),
            ("transfer_backend", ""),
        ):
            with self.subTest(field=name):
                message = self.capabilities()
                self.assertFalse(message.HasField(name))
                setattr(message, name, value)
                decoded = self.capabilities.FromString(message.SerializeToString())
                self.assertTrue(decoded.HasField(name))
                self.assertEqual(getattr(decoded, name), value)
        for values in (
            {"encoder_only": True, "supports_abort_cleanup": True},
            {"accepts_handoff": True, "requires_handoff": True},
        ):
            message = self.capabilities(schema_version=1, **values)
            self.assertEqual(
                self.capabilities.FromString(message.SerializeToString()), message
            )

    def test_encoder_mode_has_presence_and_is_exclusive(self):
        options = self.options()
        self.assertIsNone(options.WhichOneof("mode"))
        options.encode_only.SetInParent()
        encoded = options.SerializeToString()
        self.assertEqual(options.WhichOneof("mode"), "encode_only")
        options.handoff.CopyFrom(
            type(options.handoff)(transfer_backend="engine-format-v1", opaque_state=b"ref")
        )
        consumed = options.SerializeToString()
        self.assertFalse(options.HasField("encode_only"))
        self.assertEqual(options.WhichOneof("mode"), "handoff")
        self.assertEqual(
            self.options.FromString(encoded + consumed).WhichOneof("mode"), "handoff"
        )
        self.assertEqual(
            self.options.FromString(consumed + encoded).WhichOneof("mode"), "encode_only"
        )
        # The old draft bool is not a valid mode in the revised contract.
        self.assertIsNone(self.options.FromString(b"\x08\x01").WhichOneof("mode"))

    def test_additive_unknown_fields_preserve_capability_version(self):
        for message_type in (self.capabilities, self.kv_connector):
            with self.subTest(message=message_type.DESCRIPTOR.full_name):
                message = message_type(schema_version=1)
                # A future optional field 100 does not change known semantics.
                decoded = message_type.FromString(message.SerializeToString() + b"\xa0\x06\x01")
                self.assertEqual(decoded.schema_version, 1)
                self.assertTrue(decoded.HasField("schema_version"))

    def test_backend_transfer_is_outside_portable_control(self):
        self.assertNotIn("TransferEncoderCache", self.control.methods_by_name)
        self.assertIn("Abort", self.control.methods_by_name)


if __name__ == "__main__":
    unittest.main()
