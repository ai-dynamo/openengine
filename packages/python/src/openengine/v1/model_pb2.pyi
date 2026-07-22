from google.protobuf import struct_pb2 as _struct_pb2
from openengine.v1 import classification_pb2 as _classification_pb2
from openengine.v1 import embedding_pb2 as _embedding_pb2
from openengine.v1 import input_pb2 as _input_pb2
from openengine.v1 import scoring_pb2 as _scoring_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CandidateTokenSelectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CANDIDATE_TOKEN_SELECTION_MODE_UNSPECIFIED: _ClassVar[CandidateTokenSelectionMode]
    CANDIDATE_TOKEN_SELECTION_MODE_TOP_N: _ClassVar[CandidateTokenSelectionMode]
    CANDIDATE_TOKEN_SELECTION_MODE_TOKEN_IDS: _ClassVar[CandidateTokenSelectionMode]
    CANDIDATE_TOKEN_SELECTION_MODE_ALL: _ClassVar[CandidateTokenSelectionMode]

class GuidedDecodingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GUIDED_DECODING_MODE_UNSPECIFIED: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_JSON_SCHEMA: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_REGEX: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_EBNF_GRAMMAR: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_STRUCTURAL_TAG: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_CHOICE: _ClassVar[GuidedDecodingMode]
    GUIDED_DECODING_MODE_JSON_OBJECT: _ClassVar[GuidedDecodingMode]
CANDIDATE_TOKEN_SELECTION_MODE_UNSPECIFIED: CandidateTokenSelectionMode
CANDIDATE_TOKEN_SELECTION_MODE_TOP_N: CandidateTokenSelectionMode
CANDIDATE_TOKEN_SELECTION_MODE_TOKEN_IDS: CandidateTokenSelectionMode
CANDIDATE_TOKEN_SELECTION_MODE_ALL: CandidateTokenSelectionMode
GUIDED_DECODING_MODE_UNSPECIFIED: GuidedDecodingMode
GUIDED_DECODING_MODE_JSON_SCHEMA: GuidedDecodingMode
GUIDED_DECODING_MODE_REGEX: GuidedDecodingMode
GUIDED_DECODING_MODE_EBNF_GRAMMAR: GuidedDecodingMode
GUIDED_DECODING_MODE_STRUCTURAL_TAG: GuidedDecodingMode
GUIDED_DECODING_MODE_CHOICE: GuidedDecodingMode
GUIDED_DECODING_MODE_JSON_OBJECT: GuidedDecodingMode

class GetModelInfoRequest(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: str
    def __init__(self, model: _Optional[str] = ...) -> None: ...

class ModelInfo(_message.Message):
    __slots__ = ("model_id", "served_model_name", "served_model_aliases", "max_context_length", "max_output_tokens", "tokenizer_modes", "tokenizer", "supports_text_input", "supports_token_ids_input", "generation", "supports_lora", "supports_multimodal", "reasoning_parser", "tool_call_parser", "tasks", "extra", "multimodal_capabilities")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SERVED_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVED_MODEL_ALIASES_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTEXT_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_MODES_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TEXT_INPUT_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TOKEN_IDS_INPUT_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_LORA_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_MULTIMODAL_FIELD_NUMBER: _ClassVar[int]
    REASONING_PARSER_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALL_PARSER_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    MULTIMODAL_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    served_model_name: str
    served_model_aliases: _containers.RepeatedScalarFieldContainer[str]
    max_context_length: int
    max_output_tokens: int
    tokenizer_modes: _containers.RepeatedScalarFieldContainer[str]
    tokenizer: TokenizerInfo
    supports_text_input: bool
    supports_token_ids_input: bool
    generation: GenerationCapabilities
    supports_lora: bool
    supports_multimodal: bool
    reasoning_parser: str
    tool_call_parser: str
    tasks: TaskCapabilities
    extra: _struct_pb2.Struct
    multimodal_capabilities: MultimodalCapabilities
    def __init__(self, model_id: _Optional[str] = ..., served_model_name: _Optional[str] = ..., served_model_aliases: _Optional[_Iterable[str]] = ..., max_context_length: _Optional[int] = ..., max_output_tokens: _Optional[int] = ..., tokenizer_modes: _Optional[_Iterable[str]] = ..., tokenizer: _Optional[_Union[TokenizerInfo, _Mapping]] = ..., supports_text_input: _Optional[bool] = ..., supports_token_ids_input: _Optional[bool] = ..., generation: _Optional[_Union[GenerationCapabilities, _Mapping]] = ..., supports_lora: _Optional[bool] = ..., supports_multimodal: _Optional[bool] = ..., reasoning_parser: _Optional[str] = ..., tool_call_parser: _Optional[str] = ..., tasks: _Optional[_Union[TaskCapabilities, _Mapping]] = ..., extra: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., multimodal_capabilities: _Optional[_Union[MultimodalCapabilities, _Mapping]] = ...) -> None: ...

class MultimodalCapabilities(_message.Message):
    __slots__ = ("aggregate_modalities", "prefill_decode_modalities", "source_types", "supports_per_request_media_options", "routing_image_token_id")
    AGGREGATE_MODALITIES_FIELD_NUMBER: _ClassVar[int]
    PREFILL_DECODE_MODALITIES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PER_REQUEST_MEDIA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    ROUTING_IMAGE_TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    aggregate_modalities: _containers.RepeatedScalarFieldContainer[_input_pb2.Modality]
    prefill_decode_modalities: _containers.RepeatedScalarFieldContainer[_input_pb2.Modality]
    source_types: _containers.RepeatedScalarFieldContainer[_input_pb2.MediaSourceType]
    supports_per_request_media_options: bool
    routing_image_token_id: int
    def __init__(self, aggregate_modalities: _Optional[_Iterable[_Union[_input_pb2.Modality, str]]] = ..., prefill_decode_modalities: _Optional[_Iterable[_Union[_input_pb2.Modality, str]]] = ..., source_types: _Optional[_Iterable[_Union[_input_pb2.MediaSourceType, str]]] = ..., supports_per_request_media_options: _Optional[bool] = ..., routing_image_token_id: _Optional[int] = ...) -> None: ...

class TokenizerInfo(_message.Message):
    __slots__ = ("source", "mode")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    source: str
    mode: str
    def __init__(self, source: _Optional[str] = ..., mode: _Optional[str] = ...) -> None: ...

class TaskCapabilities(_message.Message):
    __slots__ = ("embed", "classify", "score")
    EMBED_FIELD_NUMBER: _ClassVar[int]
    CLASSIFY_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    embed: _embedding_pb2.EmbedCapabilities
    classify: _classification_pb2.ClassifyCapabilities
    score: _scoring_pb2.ScoreCapabilities
    def __init__(self, embed: _Optional[_Union[_embedding_pb2.EmbedCapabilities, _Mapping]] = ..., classify: _Optional[_Union[_classification_pb2.ClassifyCapabilities, _Mapping]] = ..., score: _Optional[_Union[_scoring_pb2.ScoreCapabilities, _Mapping]] = ...) -> None: ...

class GenerationCapabilities(_message.Message):
    __slots__ = ("prompt_logprobs", "output_logprobs", "guided_decoding", "max_num_sequences", "supports_priority", "supports_stop_in_output", "supports_cache_salt", "supports_prefix_cache_bypass")
    PROMPT_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    GUIDED_DECODING_FIELD_NUMBER: _ClassVar[int]
    MAX_NUM_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_STOP_IN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_CACHE_SALT_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_PREFIX_CACHE_BYPASS_FIELD_NUMBER: _ClassVar[int]
    prompt_logprobs: LogprobCapabilities
    output_logprobs: LogprobCapabilities
    guided_decoding: GuidedDecodingCapabilities
    max_num_sequences: int
    supports_priority: bool
    supports_stop_in_output: bool
    supports_cache_salt: bool
    supports_prefix_cache_bypass: bool
    def __init__(self, prompt_logprobs: _Optional[_Union[LogprobCapabilities, _Mapping]] = ..., output_logprobs: _Optional[_Union[LogprobCapabilities, _Mapping]] = ..., guided_decoding: _Optional[_Union[GuidedDecodingCapabilities, _Mapping]] = ..., max_num_sequences: _Optional[int] = ..., supports_priority: _Optional[bool] = ..., supports_stop_in_output: _Optional[bool] = ..., supports_cache_salt: _Optional[bool] = ..., supports_prefix_cache_bypass: _Optional[bool] = ...) -> None: ...

class LogprobCapabilities(_message.Message):
    __slots__ = ("supported", "candidate_selection_modes", "max_top_n")
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_SELECTION_MODES_FIELD_NUMBER: _ClassVar[int]
    MAX_TOP_N_FIELD_NUMBER: _ClassVar[int]
    supported: bool
    candidate_selection_modes: _containers.RepeatedScalarFieldContainer[CandidateTokenSelectionMode]
    max_top_n: int
    def __init__(self, supported: _Optional[bool] = ..., candidate_selection_modes: _Optional[_Iterable[_Union[CandidateTokenSelectionMode, str]]] = ..., max_top_n: _Optional[int] = ...) -> None: ...

class GuidedDecodingCapabilities(_message.Message):
    __slots__ = ("supported", "modes")
    SUPPORTED_FIELD_NUMBER: _ClassVar[int]
    MODES_FIELD_NUMBER: _ClassVar[int]
    supported: bool
    modes: _containers.RepeatedScalarFieldContainer[GuidedDecodingMode]
    def __init__(self, supported: _Optional[bool] = ..., modes: _Optional[_Iterable[_Union[GuidedDecodingMode, str]]] = ...) -> None: ...
