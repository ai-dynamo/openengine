from openengine.v1 import kv_pb2 as _kv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EngineRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENGINE_ROLE_UNSPECIFIED: _ClassVar[EngineRole]
    ENGINE_ROLE_AGGREGATED: _ClassVar[EngineRole]
    ENGINE_ROLE_PREFILL: _ClassVar[EngineRole]
    ENGINE_ROLE_DECODE: _ClassVar[EngineRole]
ENGINE_ROLE_UNSPECIFIED: EngineRole
ENGINE_ROLE_AGGREGATED: EngineRole
ENGINE_ROLE_PREFILL: EngineRole
ENGINE_ROLE_DECODE: EngineRole

class GetEngineInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EngineInfo(_message.Message):
    __slots__ = ("engine_name", "engine_version", "role", "instance_id", "supported_models", "parallelism", "kv_connector", "schema_revision", "minimum_client_revision", "schema_release")
    ENGINE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_MODELS_FIELD_NUMBER: _ClassVar[int]
    PARALLELISM_FIELD_NUMBER: _ClassVar[int]
    KV_CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_REVISION_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_CLIENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_RELEASE_FIELD_NUMBER: _ClassVar[int]
    engine_name: str
    engine_version: str
    role: EngineRole
    instance_id: str
    supported_models: _containers.RepeatedScalarFieldContainer[str]
    parallelism: ParallelismInfo
    kv_connector: _kv_pb2.KvConnectorInfo
    schema_revision: int
    minimum_client_revision: int
    schema_release: str
    def __init__(self, engine_name: _Optional[str] = ..., engine_version: _Optional[str] = ..., role: _Optional[_Union[EngineRole, str]] = ..., instance_id: _Optional[str] = ..., supported_models: _Optional[_Iterable[str]] = ..., parallelism: _Optional[_Union[ParallelismInfo, _Mapping]] = ..., kv_connector: _Optional[_Union[_kv_pb2.KvConnectorInfo, _Mapping]] = ..., schema_revision: _Optional[int] = ..., minimum_client_revision: _Optional[int] = ..., schema_release: _Optional[str] = ...) -> None: ...

class ParallelismInfo(_message.Message):
    __slots__ = ("tensor_parallel_size", "pipeline_parallel_size", "data_parallel_size", "data_parallel_rank", "data_parallel_start_rank")
    TENSOR_PARALLEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_PARALLEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_PARALLEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_PARALLEL_RANK_FIELD_NUMBER: _ClassVar[int]
    DATA_PARALLEL_START_RANK_FIELD_NUMBER: _ClassVar[int]
    tensor_parallel_size: int
    pipeline_parallel_size: int
    data_parallel_size: int
    data_parallel_rank: int
    data_parallel_start_rank: int
    def __init__(self, tensor_parallel_size: _Optional[int] = ..., pipeline_parallel_size: _Optional[int] = ..., data_parallel_size: _Optional[int] = ..., data_parallel_rank: _Optional[int] = ..., data_parallel_start_rank: _Optional[int] = ...) -> None: ...
