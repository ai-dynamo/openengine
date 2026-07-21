from google.protobuf import struct_pb2 as _struct_pb2
from openengine.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RuntimeEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNTIME_EVENT_TYPE_UNSPECIFIED: _ClassVar[RuntimeEventType]
    RUNTIME_EVENT_TYPE_FORWARD_PASS: _ClassVar[RuntimeEventType]
    RUNTIME_EVENT_TYPE_BATCH: _ClassVar[RuntimeEventType]
    RUNTIME_EVENT_TYPE_QUEUE: _ClassVar[RuntimeEventType]
    RUNTIME_EVENT_TYPE_TRANSFER: _ClassVar[RuntimeEventType]
RUNTIME_EVENT_TYPE_UNSPECIFIED: RuntimeEventType
RUNTIME_EVENT_TYPE_FORWARD_PASS: RuntimeEventType
RUNTIME_EVENT_TYPE_BATCH: RuntimeEventType
RUNTIME_EVENT_TYPE_QUEUE: RuntimeEventType
RUNTIME_EVENT_TYPE_TRANSFER: RuntimeEventType

class GetLoadRequest(_message.Message):
    __slots__ = ("include_per_rank",)
    INCLUDE_PER_RANK_FIELD_NUMBER: _ClassVar[int]
    include_per_rank: bool
    def __init__(self, include_per_rank: _Optional[bool] = ...) -> None: ...

class LoadInfo(_message.Message):
    __slots__ = ("instance_id", "timestamp_unix_nanos", "running_requests", "queued_requests", "active_kv_sessions", "used_kv_blocks", "total_kv_blocks", "running_tokens", "waiting_tokens", "prefill_batch_size", "decode_batch_size", "ranks", "attributes")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UNIX_NANOS_FIELD_NUMBER: _ClassVar[int]
    RUNNING_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    QUEUED_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_KV_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    USED_KV_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_KV_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    RUNNING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    WAITING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PREFILL_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    DECODE_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    RANKS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    timestamp_unix_nanos: int
    running_requests: int
    queued_requests: int
    active_kv_sessions: int
    used_kv_blocks: int
    total_kv_blocks: int
    running_tokens: int
    waiting_tokens: int
    prefill_batch_size: int
    decode_batch_size: int
    ranks: _containers.RepeatedCompositeFieldContainer[RankLoadInfo]
    attributes: _struct_pb2.Struct
    def __init__(self, instance_id: _Optional[str] = ..., timestamp_unix_nanos: _Optional[int] = ..., running_requests: _Optional[int] = ..., queued_requests: _Optional[int] = ..., active_kv_sessions: _Optional[int] = ..., used_kv_blocks: _Optional[int] = ..., total_kv_blocks: _Optional[int] = ..., running_tokens: _Optional[int] = ..., waiting_tokens: _Optional[int] = ..., prefill_batch_size: _Optional[int] = ..., decode_batch_size: _Optional[int] = ..., ranks: _Optional[_Iterable[_Union[RankLoadInfo, _Mapping]]] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RankLoadInfo(_message.Message):
    __slots__ = ("data_parallel_rank", "running_requests", "queued_requests", "used_kv_blocks", "total_kv_blocks", "prefill_batch_size", "decode_batch_size")
    DATA_PARALLEL_RANK_FIELD_NUMBER: _ClassVar[int]
    RUNNING_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    QUEUED_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    USED_KV_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_KV_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    PREFILL_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    DECODE_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    data_parallel_rank: int
    running_requests: int
    queued_requests: int
    used_kv_blocks: int
    total_kv_blocks: int
    prefill_batch_size: int
    decode_batch_size: int
    def __init__(self, data_parallel_rank: _Optional[int] = ..., running_requests: _Optional[int] = ..., queued_requests: _Optional[int] = ..., used_kv_blocks: _Optional[int] = ..., total_kv_blocks: _Optional[int] = ..., prefill_batch_size: _Optional[int] = ..., decode_batch_size: _Optional[int] = ...) -> None: ...

class SubscribeRuntimeEventsRequest(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[RuntimeEventType]
    def __init__(self, types: _Optional[_Iterable[_Union[RuntimeEventType, str]]] = ...) -> None: ...

class SubscribeRuntimeEventsResponse(_message.Message):
    __slots__ = ("runtime_event", "error")
    RUNTIME_EVENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    runtime_event: RuntimeEvent
    error: _error_pb2.EngineError
    def __init__(self, runtime_event: _Optional[_Union[RuntimeEvent, _Mapping]] = ..., error: _Optional[_Union[_error_pb2.EngineError, _Mapping]] = ...) -> None: ...

class RuntimeEvent(_message.Message):
    __slots__ = ("event_id", "timestamp_unix_nanos", "type", "attributes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UNIX_NANOS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    timestamp_unix_nanos: int
    type: RuntimeEventType
    attributes: _struct_pb2.Struct
    def __init__(self, event_id: _Optional[str] = ..., timestamp_unix_nanos: _Optional[int] = ..., type: _Optional[_Union[RuntimeEventType, str]] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
