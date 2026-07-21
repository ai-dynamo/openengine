from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskOutputGranularity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_OUTPUT_GRANULARITY_UNSPECIFIED: _ClassVar[TaskOutputGranularity]
    TASK_OUTPUT_GRANULARITY_SEQUENCE: _ClassVar[TaskOutputGranularity]
    TASK_OUTPUT_GRANULARITY_TOKEN: _ClassVar[TaskOutputGranularity]

class TaskValueSemantics(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_VALUE_SEMANTICS_UNSPECIFIED: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_LOGITS: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_PROBABILITIES: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_LOG_PROBABILITIES: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_SIMILARITY: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_RELEVANCE: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_REWARD: _ClassVar[TaskValueSemantics]
    TASK_VALUE_SEMANTICS_MODEL_DEFINED: _ClassVar[TaskValueSemantics]
TASK_OUTPUT_GRANULARITY_UNSPECIFIED: TaskOutputGranularity
TASK_OUTPUT_GRANULARITY_SEQUENCE: TaskOutputGranularity
TASK_OUTPUT_GRANULARITY_TOKEN: TaskOutputGranularity
TASK_VALUE_SEMANTICS_UNSPECIFIED: TaskValueSemantics
TASK_VALUE_SEMANTICS_LOGITS: TaskValueSemantics
TASK_VALUE_SEMANTICS_PROBABILITIES: TaskValueSemantics
TASK_VALUE_SEMANTICS_LOG_PROBABILITIES: TaskValueSemantics
TASK_VALUE_SEMANTICS_SIMILARITY: TaskValueSemantics
TASK_VALUE_SEMANTICS_RELEVANCE: TaskValueSemantics
TASK_VALUE_SEMANTICS_REWARD: TaskValueSemantics
TASK_VALUE_SEMANTICS_MODEL_DEFINED: TaskValueSemantics

class TaskRequestContext(_message.Message):
    __slots__ = ("request_id", "model", "lora_name", "extra")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    LORA_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    model: str
    lora_name: str
    extra: _struct_pb2.Struct
    def __init__(self, request_id: _Optional[str] = ..., model: _Optional[str] = ..., lora_name: _Optional[str] = ..., extra: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DenseFloatTensor(_message.Message):
    __slots__ = ("shape", "values")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class TaskUsage(_message.Message):
    __slots__ = ("input_tokens", "cached_input_tokens")
    INPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    CACHED_INPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    input_tokens: int
    cached_input_tokens: int
    def __init__(self, input_tokens: _Optional[int] = ..., cached_input_tokens: _Optional[int] = ...) -> None: ...
