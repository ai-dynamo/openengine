from openengine.v1 import input_pb2 as _input_pb2
from openengine.v1 import tasks_pb2 as _tasks_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScoreNormalization(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCORE_NORMALIZATION_UNSPECIFIED: _ClassVar[ScoreNormalization]
    SCORE_NORMALIZATION_NONE: _ClassVar[ScoreNormalization]
    SCORE_NORMALIZATION_SOFTMAX: _ClassVar[ScoreNormalization]
SCORE_NORMALIZATION_UNSPECIFIED: ScoreNormalization
SCORE_NORMALIZATION_NONE: ScoreNormalization
SCORE_NORMALIZATION_SOFTMAX: ScoreNormalization

class ScoreCapabilities(_message.Message):
    __slots__ = ("supported", "input_types", "granularities", "semantics", "normalizations", "supports_label_token_scoring", "supports_instruction", "max_groups", "max_candidates_per_group", "max_output_values_per_candidate", "supports_priority", "supports_lora", "higher_is_better", "modalities", "max_label_token_ids")
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    INPUT_TYPES_FIELD_NUMBER: _ClassVar[int]
    GRANULARITIES_FIELD_NUMBER: _ClassVar[int]
    SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATIONS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LABEL_TOKEN_SCORING_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    MAX_GROUPS_FIELD_NUMBER: _ClassVar[int]
    MAX_CANDIDATES_PER_GROUP_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_VALUES_PER_CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LORA_FIELD_NUMBER: _ClassVar[int]
    HIGHER_IS_BETTER_FIELD_NUMBER: _ClassVar[int]
    MODALITIES_FIELD_NUMBER: _ClassVar[int]
    MAX_LABEL_TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    supported: bool
    input_types: _containers.RepeatedScalarFieldContainer[_input_pb2.TaskInputType]
    granularities: _containers.RepeatedScalarFieldContainer[_tasks_pb2.TaskOutputGranularity]
    semantics: _containers.RepeatedScalarFieldContainer[_tasks_pb2.TaskValueSemantics]
    normalizations: _containers.RepeatedScalarFieldContainer[ScoreNormalization]
    supports_label_token_scoring: bool
    supports_instruction: bool
    max_groups: int
    max_candidates_per_group: int
    max_output_values_per_candidate: int
    supports_priority: bool
    supports_lora: bool
    higher_is_better: bool
    modalities: _containers.RepeatedScalarFieldContainer[_input_pb2.Modality]
    max_label_token_ids: int
    def __init__(self, supported: _Optional[bool] = ..., input_types: _Optional[_Iterable[_Union[_input_pb2.TaskInputType, str]]] = ..., granularities: _Optional[_Iterable[_Union[_tasks_pb2.TaskOutputGranularity, str]]] = ..., semantics: _Optional[_Iterable[_Union[_tasks_pb2.TaskValueSemantics, str]]] = ..., normalizations: _Optional[_Iterable[_Union[ScoreNormalization, str]]] = ..., supports_label_token_scoring: _Optional[bool] = ..., supports_instruction: _Optional[bool] = ..., max_groups: _Optional[int] = ..., max_candidates_per_group: _Optional[int] = ..., max_output_values_per_candidate: _Optional[int] = ..., supports_priority: _Optional[bool] = ..., supports_lora: _Optional[bool] = ..., higher_is_better: _Optional[bool] = ..., modalities: _Optional[_Iterable[_Union[_input_pb2.Modality, str]]] = ..., max_label_token_ids: _Optional[int] = ...) -> None: ...

class ScoreRequest(_message.Message):
    __slots__ = ("context", "groups", "options")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    context: _tasks_pb2.TaskRequestContext
    groups: _containers.RepeatedCompositeFieldContainer[ScoreGroup]
    options: ScoreOptions
    def __init__(self, context: _Optional[_Union[_tasks_pb2.TaskRequestContext, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[ScoreGroup, _Mapping]]] = ..., options: _Optional[_Union[ScoreOptions, _Mapping]] = ...) -> None: ...

class ScoreGroup(_message.Message):
    __slots__ = ("group_id", "query", "candidates")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    query: _input_pb2.TaskInput
    candidates: _containers.RepeatedCompositeFieldContainer[_input_pb2.TaskInput]
    def __init__(self, group_id: _Optional[str] = ..., query: _Optional[_Union[_input_pb2.TaskInput, _Mapping]] = ..., candidates: _Optional[_Iterable[_Union[_input_pb2.TaskInput, _Mapping]]] = ...) -> None: ...

class ScoreOptions(_message.Message):
    __slots__ = ("granularity", "output_semantics", "normalization", "label_token_ids", "instruction")
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATION_FIELD_NUMBER: _ClassVar[int]
    LABEL_TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    granularity: _tasks_pb2.TaskOutputGranularity
    output_semantics: _tasks_pb2.TaskValueSemantics
    normalization: ScoreNormalization
    label_token_ids: _containers.RepeatedScalarFieldContainer[int]
    instruction: str
    def __init__(self, granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., output_semantics: _Optional[_Union[_tasks_pb2.TaskValueSemantics, str]] = ..., normalization: _Optional[_Union[ScoreNormalization, str]] = ..., label_token_ids: _Optional[_Iterable[int]] = ..., instruction: _Optional[str] = ...) -> None: ...

class ScoreResponse(_message.Message):
    __slots__ = ("request_id", "groups", "granularity", "semantics", "higher_is_better", "normalization", "label_token_ids", "usage")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    SEMANTICS_FIELD_NUMBER: _ClassVar[int]
    HIGHER_IS_BETTER_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATION_FIELD_NUMBER: _ClassVar[int]
    LABEL_TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    groups: _containers.RepeatedCompositeFieldContainer[ScoreGroupOutput]
    granularity: _tasks_pb2.TaskOutputGranularity
    semantics: _tasks_pb2.TaskValueSemantics
    higher_is_better: bool
    normalization: ScoreNormalization
    label_token_ids: _containers.RepeatedScalarFieldContainer[int]
    usage: _tasks_pb2.TaskUsage
    def __init__(self, request_id: _Optional[str] = ..., groups: _Optional[_Iterable[_Union[ScoreGroupOutput, _Mapping]]] = ..., granularity: _Optional[_Union[_tasks_pb2.TaskOutputGranularity, str]] = ..., semantics: _Optional[_Union[_tasks_pb2.TaskValueSemantics, str]] = ..., higher_is_better: _Optional[bool] = ..., normalization: _Optional[_Union[ScoreNormalization, str]] = ..., label_token_ids: _Optional[_Iterable[int]] = ..., usage: _Optional[_Union[_tasks_pb2.TaskUsage, _Mapping]] = ...) -> None: ...

class ScoreGroupOutput(_message.Message):
    __slots__ = ("group_id", "group_index", "candidates")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_INDEX_FIELD_NUMBER: _ClassVar[int]
    CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    group_index: int
    candidates: _containers.RepeatedCompositeFieldContainer[ScoreCandidateOutput]
    def __init__(self, group_id: _Optional[str] = ..., group_index: _Optional[int] = ..., candidates: _Optional[_Iterable[_Union[ScoreCandidateOutput, _Mapping]]] = ...) -> None: ...

class ScoreCandidateOutput(_message.Message):
    __slots__ = ("candidate_id", "candidate_index", "scores", "token_ids")
    CANDIDATE_ID_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    candidate_id: str
    candidate_index: int
    scores: _tasks_pb2.DenseFloatTensor
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, candidate_id: _Optional[str] = ..., candidate_index: _Optional[int] = ..., scores: _Optional[_Union[_tasks_pb2.DenseFloatTensor, _Mapping]] = ..., token_ids: _Optional[_Iterable[int]] = ...) -> None: ...
