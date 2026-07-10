import unittest

import grpc

from openengine import SCHEMA_RELEASE, SCHEMA_REVISION, __version__
from openengine.v1.generation_pb2 import GenerateRequest
from openengine.v1.openengine_pb2_grpc import OpenEngineStub


class BindingsTest(unittest.TestCase):
    def test_request_round_trip_preserves_optional_zero(self) -> None:
        request = GenerateRequest(
            request_id="python-smoke",
            model="test-model",
            prompt="Hello",
            priority=0,
        )

        decoded = GenerateRequest.FromString(request.SerializeToString())

        self.assertEqual(decoded.request_id, "python-smoke")
        self.assertEqual(decoded.WhichOneof("input"), "prompt")
        self.assertTrue(decoded.HasField("priority"))
        self.assertEqual(decoded.priority, 0)

    def test_client_stub_can_be_constructed(self) -> None:
        channel = grpc.insecure_channel("localhost:1")
        self.addCleanup(channel.close)

        stub = OpenEngineStub(channel)

        self.assertTrue(callable(stub.Generate))
        self.assertTrue(callable(stub.GetEngineInfo))

    def test_package_metadata_matches_schema(self) -> None:
        self.assertEqual(SCHEMA_REVISION, 1)
        self.assertEqual(SCHEMA_RELEASE, f"v{__version__}")


if __name__ == "__main__":
    unittest.main()
