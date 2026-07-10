from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ARGUMENT: _ClassVar[ErrorCode]
    ERROR_CODE_UNSUPPORTED_FEATURE: _ClassVar[ErrorCode]
    ERROR_CODE_ROLE_MISMATCH: _ClassVar[ErrorCode]
    ERROR_CODE_MODEL_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_OVERLOADED: _ClassVar[ErrorCode]
    ERROR_CODE_REQUEST_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_DUPLICATE_REQUEST: _ClassVar[ErrorCode]
    ERROR_CODE_KV_SESSION_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_KV_TRANSFER_FAILED: _ClassVar[ErrorCode]
    ERROR_CODE_CANCELLED: _ClassVar[ErrorCode]
    ERROR_CODE_DRAINING: _ClassVar[ErrorCode]
    ERROR_CODE_INTERNAL: _ClassVar[ErrorCode]
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_INVALID_ARGUMENT: ErrorCode
ERROR_CODE_UNSUPPORTED_FEATURE: ErrorCode
ERROR_CODE_ROLE_MISMATCH: ErrorCode
ERROR_CODE_MODEL_NOT_FOUND: ErrorCode
ERROR_CODE_OVERLOADED: ErrorCode
ERROR_CODE_REQUEST_NOT_FOUND: ErrorCode
ERROR_CODE_DUPLICATE_REQUEST: ErrorCode
ERROR_CODE_KV_SESSION_NOT_FOUND: ErrorCode
ERROR_CODE_KV_TRANSFER_FAILED: ErrorCode
ERROR_CODE_CANCELLED: ErrorCode
ERROR_CODE_DRAINING: ErrorCode
ERROR_CODE_INTERNAL: ErrorCode

class EngineError(_message.Message):
    __slots__ = ("code", "message", "retryable", "retry_after_ms", "details")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RETRYABLE_FIELD_NUMBER: _ClassVar[int]
    RETRY_AFTER_MS_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    retryable: bool
    retry_after_ms: int
    details: _struct_pb2.Struct
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ..., retryable: _Optional[bool] = ..., retry_after_ms: _Optional[int] = ..., details: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
