from openengine.v1 import kv_pb2 as _kv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TokenIds(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ids: _Optional[_Iterable[int]] = ...) -> None: ...

class SamplingParams(_message.Message):
    __slots__ = ("temperature", "top_p", "top_k", "min_p", "frequency_penalty", "presence_penalty", "repetition_penalty", "seed", "num_sequences")
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    MIN_P_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_PENALTY_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    NUM_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    temperature: float
    top_p: float
    top_k: int
    min_p: float
    frequency_penalty: float
    presence_penalty: float
    repetition_penalty: float
    seed: int
    num_sequences: int
    def __init__(self, temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., top_k: _Optional[int] = ..., min_p: _Optional[float] = ..., frequency_penalty: _Optional[float] = ..., presence_penalty: _Optional[float] = ..., repetition_penalty: _Optional[float] = ..., seed: _Optional[int] = ..., num_sequences: _Optional[int] = ...) -> None: ...

class StoppingOptions(_message.Message):
    __slots__ = ("max_tokens", "min_tokens", "conditions", "ignore_eos", "include_stop_in_output")
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MIN_TOKENS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORE_EOS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_STOP_IN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    max_tokens: int
    min_tokens: int
    conditions: _containers.RepeatedCompositeFieldContainer[StopCondition]
    ignore_eos: bool
    include_stop_in_output: bool
    def __init__(self, max_tokens: _Optional[int] = ..., min_tokens: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[StopCondition, _Mapping]]] = ..., ignore_eos: _Optional[bool] = ..., include_stop_in_output: _Optional[bool] = ...) -> None: ...

class ResponseOptions(_message.Message):
    __slots__ = ("return_prompt_logprobs", "prompt_candidates", "return_output_logprobs", "output_candidates", "prompt_logprob_start")
    RETURN_PROMPT_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    RETURN_OUTPUT_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    PROMPT_LOGPROB_START_FIELD_NUMBER: _ClassVar[int]
    return_prompt_logprobs: bool
    prompt_candidates: CandidateTokenSelection
    return_output_logprobs: bool
    output_candidates: CandidateTokenSelection
    prompt_logprob_start: int
    def __init__(self, return_prompt_logprobs: _Optional[bool] = ..., prompt_candidates: _Optional[_Union[CandidateTokenSelection, _Mapping]] = ..., return_output_logprobs: _Optional[bool] = ..., output_candidates: _Optional[_Union[CandidateTokenSelection, _Mapping]] = ..., prompt_logprob_start: _Optional[int] = ...) -> None: ...

class CandidateTokenSelection(_message.Message):
    __slots__ = ("top_n", "token_ids", "all")
    TOP_N_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    ALL_FIELD_NUMBER: _ClassVar[int]
    top_n: int
    token_ids: TokenIds
    all: AllCandidates
    def __init__(self, top_n: _Optional[int] = ..., token_ids: _Optional[_Union[TokenIds, _Mapping]] = ..., all: _Optional[_Union[AllCandidates, _Mapping]] = ...) -> None: ...

class AllCandidates(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KvOptions(_message.Message):
    __slots__ = ("session", "data_parallel_rank", "bypass_prefix_cache", "cache_salt")
    SESSION_FIELD_NUMBER: _ClassVar[int]
    DATA_PARALLEL_RANK_FIELD_NUMBER: _ClassVar[int]
    BYPASS_PREFIX_CACHE_FIELD_NUMBER: _ClassVar[int]
    CACHE_SALT_FIELD_NUMBER: _ClassVar[int]
    session: _kv_pb2.KvSessionRef
    data_parallel_rank: int
    bypass_prefix_cache: bool
    cache_salt: str
    def __init__(self, session: _Optional[_Union[_kv_pb2.KvSessionRef, _Mapping]] = ..., data_parallel_rank: _Optional[int] = ..., bypass_prefix_cache: _Optional[bool] = ..., cache_salt: _Optional[str] = ...) -> None: ...

class StopCondition(_message.Message):
    __slots__ = ("stop_text", "stop_token_id")
    STOP_TEXT_FIELD_NUMBER: _ClassVar[int]
    STOP_TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    stop_text: str
    stop_token_id: int
    def __init__(self, stop_text: _Optional[str] = ..., stop_token_id: _Optional[int] = ...) -> None: ...

class GuidedDecoding(_message.Message):
    __slots__ = ("json_schema", "regex", "ebnf_grammar", "structural_tag", "choice", "json_object", "backend")
    JSON_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    REGEX_FIELD_NUMBER: _ClassVar[int]
    EBNF_GRAMMAR_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_TAG_FIELD_NUMBER: _ClassVar[int]
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    JSON_OBJECT_FIELD_NUMBER: _ClassVar[int]
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    json_schema: str
    regex: str
    ebnf_grammar: str
    structural_tag: str
    choice: ChoiceConstraint
    json_object: JsonObjectConstraint
    backend: str
    def __init__(self, json_schema: _Optional[str] = ..., regex: _Optional[str] = ..., ebnf_grammar: _Optional[str] = ..., structural_tag: _Optional[str] = ..., choice: _Optional[_Union[ChoiceConstraint, _Mapping]] = ..., json_object: _Optional[_Union[JsonObjectConstraint, _Mapping]] = ..., backend: _Optional[str] = ...) -> None: ...

class ChoiceConstraint(_message.Message):
    __slots__ = ("choices",)
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    choices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, choices: _Optional[_Iterable[str]] = ...) -> None: ...

class JsonObjectConstraint(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
