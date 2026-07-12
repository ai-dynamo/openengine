from openengine.v1 import input_pb2 as _input_pb2
from openengine.v1 import tasks_pb2 as _tasks_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClassifyCapabilities(_message.Message):
    __slots__ = ("supported", "input_types", "granularities", "semantics", "max_batch_size", "max_output_values_per_item", "supports_priority", "supports_lora", "modalities")
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    GRANULARITIES_FIELD_NUMBER: _ClassVar[int]
    SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    MAX_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_VALUES_PER_ITEM_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LORA_FIELD_NUMBER: _ClassVar[int]
    MODALITIES_FIELD_NUMBER: _ClassVar[int]
    supported: bool
    input_types: _containers.RepeatedScalarFieldContainer[_input_pb2.TaskInputType]
    granularities: _containers.RepeatedScalarFieldContainer[_tasks_pb2.TaskOutputGranularity]
    semantics: _containers.RepeatedScalarFieldContainer[_tasks_pb2.TaskValueSemantics]
    max_batch_size: int
    max_output_values_per_item: int
    supports_priority: bool
    supports_lora: bool
    modalities: _containers.RepeatedScalarFieldContainer[_input_pb2.Modality]
    def __init__(self, supported: _Optional[bool] = ..., input_types: _Optional[_Iterable[_Union[_input_pb2.TaskInputType, str]]] = ..., granularities: _Optional[_Iterable[_Union[_tasks_pb2.TaskOutputGranularity, str]]] = ..., semantics: _Optional[_Iterable[_Union[_tasks_pb2.TaskValueSemantics, str]]] = ..., max_batch_size: _Optional[int] = ..., max_output_values_per_item: _Optional[int] = ..., supports_priority: _Optional[bool] = ..., supports_lora: _Optional[bool] = ..., modalities: _Optional[_Iterable[_Union[_input_pb2.Modality, str]]] = ...) -> None: ...

class ClassifyRequest(_message.Message):
    __slots__ = ("context", "inputs", "options")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    context: _tasks_pb2.TaskRequestContext
    inputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.TaskInput]
    options: ClassifyOptions
    def __init__(self, context: _Optional[_Union[_tasks_pb2.TaskRequestContext, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[_input_pb2.TaskInput, _Mapping]]] = ..., options: _Optional[_Union[ClassifyOptions, _Mapping]] = ...) -> None: ...

class ClassifyOptions(_message.Message):
    __slots__ = ("granularity", "output_semantics")
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    granularity: _tasks_pb2.TaskOutputGranularity
    output_semantics: _tasks_pb2.TaskValueSemantics
    def __init__(self, granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., output_semantics: _Optional[_Union[_tasks_pb2.TaskValueSemantics, str]] = ...) -> None: ...

class ClassifyResponse(_message.Message):
    __slots__ = ("request_id", "outputs", "usage")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[ClassificationOutput]
    usage: _tasks_pb2.TaskUsage
    def __init__(self, request_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[ClassificationOutput, _Mapping]]] = ..., usage: _Optional[_Union[_tasks_pb2.TaskUsage, _Mapping]] = ...) -> None: ...

class ClassificationOutput(_message.Message):
    __slots__ = ("item_id", "input_index", "granularity", "semantics", "scores", "labels", "token_ids")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    input_index: int
    granularity: _tasks_pb2.TaskOutputGranularity
    semantics: _tasks_pb2.TaskValueSemantics
    scores: _tasks_pb2.DenseFloatTensor
    labels: _containers.RepeatedScalarFieldContainer[str]
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_id: _Optional[str] = ..., input_index: _Optional[int] = ..., granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., semantics: _Optional[_Union[_tasks_pb2.TaskValueSemantics, str]] = ..., scores: _Optional[_Union[_tasks_pb2.DenseFloatTensor, _Mapping]] = ..., labels: _Optional[_Iterable[str]] = ..., token_ids: _Optional[_Iterable[int]] = ...) -> None: ...
