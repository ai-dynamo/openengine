from openengine.v1 import input_pb2 as _input_pb2
from openengine.v1 import tasks_pb2 as _tasks_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddingEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMBEDDING_ENCODING_UNSPECIFIED: _ClassVar[EmbeddingEncoding]
    EMBEDDING_ENCODING_DENSE: _ClassVar[EmbeddingEncoding]
    EMBEDDING_ENCODING_SPARSE: _ClassVar[EmbeddingEncoding]
EMBEDDING_ENCODING_UNSPECIFIED: EmbeddingEncoding
EMBEDDING_ENCODING_DENSE: EmbeddingEncoding
EMBEDDING_ENCODING_SPARSE: EmbeddingEncoding

class SparseFloatTensor(_message.Message):
    __slots__ = ("shape", "indices", "values")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    INDICES_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    indices: _containers.RepeatedScalarFieldContainer[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., indices: _Optional[_Iterable[int]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class EmbedCapabilities(_message.Message):
    __slots__ = ("supported", "input_types", "granularities", "encodings", "dimension", "max_batch_size", "max_output_values_per_item", "supports_priority", "supports_lora", "supports_normalization", "supports_dimension_override", "modalities")
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    GRANULARITIES_FIELD_NUMBER: _ClassVar[int]
    ENCODINGS_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    MAX_BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_VALUES_PER_ITEM_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LORA_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_NORMALIZATION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_DIMENSION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    MODALITIES_FIELD_NUMBER: _ClassVar[int]
    supported: bool
    input_types: _containers.RepeatedScalarFieldContainer[_input_pb2.TaskInputType]
    granularities: _containers.RepeatedScalarFieldContainer[_tasks_pb2.TaskOutputGranularity]
    encodings: _containers.RepeatedScalarFieldContainer[EmbeddingEncoding]
    dimension: int
    max_batch_size: int
    max_output_values_per_item: int
    supports_priority: bool
    supports_lora: bool
    supports_normalization: bool
    supports_dimension_override: bool
    modalities: _containers.RepeatedScalarFieldContainer[_input_pb2.Modality]
    def __init__(self, supported: _Optional[bool] = ..., input_types: _Optional[_Iterable[_Union[_input_pb2.TaskInputType, str]]] = ..., granularities: _Optional[_Iterable[_Union[_tasks_pb2.TaskOutputGranularity, str]]] = ..., encodings: _Optional[_Iterable[_Union[EmbeddingEncoding, str]]] = ..., dimension: _Optional[int] = ..., max_batch_size: _Optional[int] = ..., max_output_values_per_item: _Optional[int] = ..., supports_priority: _Optional[bool] = ..., supports_lora: _Optional[bool] = ..., supports_normalization: _Optional[bool] = ..., supports_dimension_override: _Optional[bool] = ..., modalities: _Optional[_Iterable[_Union[_input_pb2.Modality, str]]] = ...) -> None: ...

class EmbedRequest(_message.Message):
    __slots__ = ("context", "inputs", "options")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    context: _tasks_pb2.TaskRequestContext
    inputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.TaskInput]
    options: EmbedOptions
    def __init__(self, context: _Optional[_Union[_tasks_pb2.TaskRequestContext, _Mapping]] = ..., inputs: _Optional[_Iterable[_Union[_input_pb2.TaskInput, _Mapping]]] = ..., options: _Optional[_Union[EmbedOptions, _Mapping]] = ...) -> None: ...

class EmbedOptions(_message.Message):
    __slots__ = ("granularity", "normalize", "dimensions", "encoding")
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    NORMALIZE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    granularity: _tasks_pb2.TaskOutputGranularity
    normalize: bool
    dimensions: int
    encoding: EmbeddingEncoding
    def __init__(self, granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., normalize: _Optional[bool] = ..., dimensions: _Optional[int] = ..., encoding: _Optional[_Union[EmbeddingEncoding, str]] = ...) -> None: ...

class EmbedResponse(_message.Message):
    __slots__ = ("request_id", "outputs", "usage")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    outputs: _containers.RepeatedCompositeFieldContainer[EmbeddingOutput]
    usage: _tasks_pb2.TaskUsage
    def __init__(self, request_id: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[EmbeddingOutput, _Mapping]]] = ..., usage: _Optional[_Union[_tasks_pb2.TaskUsage, _Mapping]] = ...) -> None: ...

class EmbeddingOutput(_message.Message):
    __slots__ = ("item_id", "input_index", "granularity", "dense", "sparse", "token_ids")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    DENSE_FIELD_NUMBER: _ClassVar[int]
    SPARSE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    input_index: int
    granularity: _tasks_pb2.TaskOutputGranularity
    dense: _tasks_pb2.DenseFloatTensor
    sparse: SparseFloatTensor
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_id: _Optional[str] = ..., input_index: _Optional[int] = ..., granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., dense: _Optional[_Union[_tasks_pb2.DenseFloatTensor, _Mapping]] = ..., sparse: _Optional[_Union[SparseFloatTensor, _Mapping]] = ..., token_ids: _Optional[_Iterable[int]] = ...) -> None: ...
