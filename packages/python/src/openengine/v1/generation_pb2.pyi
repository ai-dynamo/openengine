from openengine.v1 import error_pb2 as _error_pb2
from openengine.v1 import generation_params_pb2 as _generation_params_pb2
from openengine.v1 import kv_pb2 as _kv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Modality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODALITY_UNSPECIFIED: _ClassVar[Modality]
    MODALITY_IMAGE: _ClassVar[Modality]
    MODALITY_VIDEO: _ClassVar[Modality]
    MODALITY_AUDIO: _ClassVar[Modality]

class FinishReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FINISH_REASON_UNSPECIFIED: _ClassVar[FinishReason]
    FINISH_REASON_STOP: _ClassVar[FinishReason]
    FINISH_REASON_LENGTH: _ClassVar[FinishReason]
    FINISH_REASON_CANCELLED: _ClassVar[FinishReason]
MODALITY_UNSPECIFIED: Modality
MODALITY_IMAGE: Modality
MODALITY_VIDEO: Modality
MODALITY_AUDIO: Modality
FINISH_REASON_UNSPECIFIED: FinishReason
FINISH_REASON_STOP: FinishReason
FINISH_REASON_LENGTH: FinishReason
FINISH_REASON_CANCELLED: FinishReason

class GenerateRequest(_message.Message):
    __slots__ = ("request_id", "model", "prompt", "token_ids", "sampling", "stopping", "response", "kv", "guided", "media", "lora_name", "priority", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_FIELD_NUMBER: _ClassVar[int]
    STOPPING_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    KV_FIELD_NUMBER: _ClassVar[int]
    GUIDED_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    LORA_NAME_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    model: str
    prompt: str
    token_ids: _generation_params_pb2.TokenIds
    sampling: _generation_params_pb2.SamplingParams
    stopping: _generation_params_pb2.StoppingOptions
    response: _generation_params_pb2.ResponseOptions
    kv: _generation_params_pb2.KvOptions
    guided: _generation_params_pb2.GuidedDecoding
    media: _containers.RepeatedCompositeFieldContainer[MediaItem]
    lora_name: str
    priority: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, request_id: _Optional[str] = ..., model: _Optional[str] = ..., prompt: _Optional[str] = ..., token_ids: _Optional[_Union[_generation_params_pb2.TokenIds, _Mapping]] = ..., sampling: _Optional[_Union[_generation_params_pb2.SamplingParams, _Mapping]] = ..., stopping: _Optional[_Union[_generation_params_pb2.StoppingOptions, _Mapping]] = ..., response: _Optional[_Union[_generation_params_pb2.ResponseOptions, _Mapping]] = ..., kv: _Optional[_Union[_generation_params_pb2.KvOptions, _Mapping]] = ..., guided: _Optional[_Union[_generation_params_pb2.GuidedDecoding, _Mapping]] = ..., media: _Optional[_Iterable[_Union[MediaItem, _Mapping]]] = ..., lora_name: _Optional[str] = ..., priority: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MediaItem(_message.Message):
    __slots__ = ("modality", "url", "data_uri", "raw_bytes", "mime_type", "uuid")
    MODALITY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATA_URI_FIELD_NUMBER: _ClassVar[int]
    RAW_BYTES_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    modality: Modality
    url: str
    data_uri: str
    raw_bytes: bytes
    mime_type: str
    uuid: str
    def __init__(self, modality: _Optional[_Union[Modality, str]] = ..., url: _Optional[str] = ..., data_uri: _Optional[str] = ..., raw_bytes: _Optional[bytes] = ..., mime_type: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class GenerateResponse(_message.Message):
    __slots__ = ("request_id", "prompt", "token", "prefill_ready", "finished", "error", "usage")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREFILL_READY_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    prompt: PromptOutput
    token: TokenOutput
    prefill_ready: PrefillReady
    finished: GenerationFinished
    error: _error_pb2.EngineError
    usage: Usage
    def __init__(self, request_id: _Optional[str] = ..., prompt: _Optional[_Union[PromptOutput, _Mapping]] = ..., token: _Optional[_Union[TokenOutput, _Mapping]] = ..., prefill_ready: _Optional[_Union[PrefillReady, _Mapping]] = ..., finished: _Optional[_Union[GenerationFinished, _Mapping]] = ..., error: _Optional[_Union[_error_pb2.EngineError, _Mapping]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

class PromptOutput(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[TokenInfo]
    def __init__(self, tokens: _Optional[_Iterable[_Union[TokenInfo, _Mapping]]] = ...) -> None: ...

class TokenOutput(_message.Message):
    __slots__ = ("output_index", "tokens", "text")
    OUTPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    output_index: int
    tokens: _containers.RepeatedCompositeFieldContainer[TokenInfo]
    text: str
    def __init__(self, output_index: _Optional[int] = ..., tokens: _Optional[_Iterable[_Union[TokenInfo, _Mapping]]] = ..., text: _Optional[str] = ...) -> None: ...

class TokenInfo(_message.Message):
    __slots__ = ("token_id", "token", "logprob", "rank", "candidates")
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    LOGPROB_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    token: str
    logprob: float
    rank: int
    candidates: _containers.RepeatedCompositeFieldContainer[LogProb]
    def __init__(self, token_id: _Optional[int] = ..., token: _Optional[str] = ..., logprob: _Optional[float] = ..., rank: _Optional[int] = ..., candidates: _Optional[_Iterable[_Union[LogProb, _Mapping]]] = ...) -> None: ...

class LogProb(_message.Message):
    __slots__ = ("token_id", "logprob", "token", "rank")
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    LOGPROB_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    logprob: float
    token: str
    rank: int
    def __init__(self, token_id: _Optional[int] = ..., logprob: _Optional[float] = ..., token: _Optional[str] = ..., rank: _Optional[int] = ...) -> None: ...

class PrefillReady(_message.Message):
    __slots__ = ("kv_session",)
    KV_SESSION_FIELD_NUMBER: _ClassVar[int]
    kv_session: _kv_pb2.KvSessionRef
    def __init__(self, kv_session: _Optional[_Union[_kv_pb2.KvSessionRef, _Mapping]] = ...) -> None: ...

class GenerationFinished(_message.Message):
    __slots__ = ("output_index", "reason", "message", "stop_match")
    OUTPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STOP_MATCH_FIELD_NUMBER: _ClassVar[int]
    output_index: int
    reason: FinishReason
    message: str
    stop_match: StopMatch
    def __init__(self, output_index: _Optional[int] = ..., reason: _Optional[_Union[FinishReason, str]] = ..., message: _Optional[str] = ..., stop_match: _Optional[_Union[StopMatch, _Mapping]] = ...) -> None: ...

class StopMatch(_message.Message):
    __slots__ = ("stop_token_id", "stop_text", "eos_token_id")
    STOP_TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    STOP_TEXT_FIELD_NUMBER: _ClassVar[int]
    EOS_TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    stop_token_id: int
    stop_text: str
    eos_token_id: int
    def __init__(self, stop_token_id: _Optional[int] = ..., stop_text: _Optional[str] = ..., eos_token_id: _Optional[int] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "total_tokens", "cached_prompt_tokens", "reasoning_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    CACHED_PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    REASONING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cached_prompt_tokens: int
    reasoning_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ..., cached_prompt_tokens: _Optional[int] = ..., reasoning_tokens: _Optional[int] = ...) -> None: ...
