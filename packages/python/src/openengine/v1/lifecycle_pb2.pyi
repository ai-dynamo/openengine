from openengine.v1 import error_pb2 as _error_pb2
from openengine.v1 import kv_pb2 as _kv_pb2
from openengine.v1 import server_pb2 as _server_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HealthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_STATE_UNSPECIFIED: _ClassVar[HealthState]
    HEALTH_STATE_STARTING: _ClassVar[HealthState]
    HEALTH_STATE_READY: _ClassVar[HealthState]
    HEALTH_STATE_DEGRADED: _ClassVar[HealthState]
    HEALTH_STATE_DRAINING: _ClassVar[HealthState]
    HEALTH_STATE_NOT_READY: _ClassVar[HealthState]

class AbortStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ABORT_STATUS_UNSPECIFIED: _ClassVar[AbortStatus]
    ABORT_STATUS_ABORTED: _ClassVar[AbortStatus]
    ABORT_STATUS_ALREADY_FINISHED: _ClassVar[AbortStatus]

class DrainState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRAIN_STATE_UNSPECIFIED: _ClassVar[DrainState]
    DRAIN_STATE_STARTED: _ClassVar[DrainState]
    DRAIN_STATE_IN_PROGRESS: _ClassVar[DrainState]
    DRAIN_STATE_COMPLETE: _ClassVar[DrainState]
HEALTH_STATE_UNSPECIFIED: HealthState
HEALTH_STATE_STARTING: HealthState
HEALTH_STATE_READY: HealthState
HEALTH_STATE_DEGRADED: HealthState
HEALTH_STATE_DRAINING: HealthState
HEALTH_STATE_NOT_READY: HealthState
ABORT_STATUS_UNSPECIFIED: AbortStatus
ABORT_STATUS_ABORTED: AbortStatus
ABORT_STATUS_ALREADY_FINISHED: AbortStatus
DRAIN_STATE_UNSPECIFIED: DrainState
DRAIN_STATE_STARTED: DrainState
DRAIN_STATE_IN_PROGRESS: DrainState
DRAIN_STATE_COMPLETE: DrainState

class HealthRequest(_message.Message):
    __slots__ = ("include_inference_probe", "model", "role")
    INCLUDE_INFERENCE_PROBE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    include_inference_probe: bool
    model: str
    role: _server_pb2.EngineRole
    def __init__(self, include_inference_probe: _Optional[bool] = ..., model: _Optional[str] = ..., role: _Optional[_Union[_server_pb2.EngineRole, str]] = ...) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ("state", "checks")
    STATE_FIELD_NUMBER: _ClassVar[int]
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    state: HealthState
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, state: _Optional[_Union[HealthState, str]] = ..., checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class HealthCheck(_message.Message):
    __slots__ = ("name", "state", "message")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    state: HealthState
    message: str
    def __init__(self, name: _Optional[str] = ..., state: _Optional[_Union[HealthState, str]] = ..., message: _Optional[str] = ...) -> None: ...

class AbortRequest(_message.Message):
    __slots__ = ("request_id", "kv_session", "all_requests")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    KV_SESSION_FIELD_NUMBER: _ClassVar[int]
    ALL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    kv_session: _kv_pb2.KvSessionRef
    all_requests: AllRequests
    def __init__(self, request_id: _Optional[str] = ..., kv_session: _Optional[_Union[_kv_pb2.KvSessionRef, _Mapping]] = ..., all_requests: _Optional[_Union[AllRequests, _Mapping]] = ...) -> None: ...

class AllRequests(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AbortResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: AbortStatus
    message: str
    def __init__(self, status: _Optional[_Union[AbortStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class DrainRequest(_message.Message):
    __slots__ = ("stop_accepting_new_requests", "deadline_ms", "abort_after_deadline")
    STOP_ACCEPTING_NEW_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_MS_FIELD_NUMBER: _ClassVar[int]
    ABORT_AFTER_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    stop_accepting_new_requests: bool
    deadline_ms: int
    abort_after_deadline: bool
    def __init__(self, stop_accepting_new_requests: _Optional[bool] = ..., deadline_ms: _Optional[int] = ..., abort_after_deadline: _Optional[bool] = ...) -> None: ...

class DrainResponse(_message.Message):
    __slots__ = ("state", "error", "in_flight_requests", "open_kv_sessions", "message")
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IN_FLIGHT_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    OPEN_KV_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    state: DrainState
    error: _error_pb2.EngineError
    in_flight_requests: int
    open_kv_sessions: int
    message: str
    def __init__(self, state: _Optional[_Union[DrainState, str]] = ..., error: _Optional[_Union[_error_pb2.EngineError, _Mapping]] = ..., in_flight_requests: _Optional[int] = ..., open_kv_sessions: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
