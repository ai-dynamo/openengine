<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# OpenEngine API v1

This is the human-readable reference for [`openengine.v1`](../proto/openengine.proto).
The proto is the source of truth.

---

## Service overview

```protobuf
syntax = "proto3";

package openengine.v1;

import "google/protobuf/struct.proto";

service OpenEngine {
  // Core inference path.
  rpc Generate(GenerateRequest) returns (stream GenerateResponse);

  // Runtime metadata and scheduling state.
  rpc GetEngineInfo(GetEngineInfoRequest) returns (EngineInfo);
  rpc GetModelInfo(GetModelInfoRequest) returns (ModelInfo);
  rpc GetLoad(GetLoadRequest) returns (LoadInfo);

  // Health and lifecycle.
  rpc Health(HealthRequest) returns (HealthResponse);
  rpc Abort(AbortRequest) returns (AbortResponse);
  rpc Drain(DrainRequest) returns (stream DrainResponse);

  // LoRA lifecycle.
  rpc LoadLora(LoadLoraRequest) returns (LoadLoraResponse);
  rpc UnloadLora(UnloadLoraRequest) returns (UnloadLoraResponse);
  rpc ListLoras(ListLorasRequest) returns (ListLorasResponse);

  // Disaggregated serving / KV transfer.
  rpc GetKvConnectorInfo(GetKvConnectorInfoRequest) returns (KvConnectorInfo);
  rpc GetKvEventSources(GetKvEventSourcesRequest) returns (GetKvEventSourcesResponse);
  rpc SubscribeKvEvents(SubscribeKvEventsRequest) returns (stream SubscribeKvEventsResponse);

  // Structured runtime events for planners/controllers.
  rpc SubscribeRuntimeEvents(SubscribeRuntimeEventsRequest) returns (stream SubscribeRuntimeEventsResponse);
}
```

---

## Core identity and roles

```protobuf
enum EngineRole {
  ENGINE_ROLE_UNSPECIFIED = 0;
  ENGINE_ROLE_AGGREGATED = 1;
  ENGINE_ROLE_PREFILL = 2;
  ENGINE_ROLE_DECODE = 3;
}

message GetEngineInfoRequest {}

message EngineInfo {
  string engine_name = 1;          // sglang, vllm, tensorrt_llm, etc.
  string engine_version = 2;
  EngineRole role = 3;
  string instance_id = 4;
  repeated string supported_models = 5;
  ParallelismInfo parallelism = 6;
  KvConnectorInfo kv_connector = 7;
  uint32 schema_revision = 8;
  uint32 minimum_client_revision = 9;
  string schema_release = 10;
}

message ParallelismInfo {
  optional uint32 tensor_parallel_size = 1;
  optional uint32 pipeline_parallel_size = 2;
  optional uint32 data_parallel_size = 3;
  optional uint32 data_parallel_rank = 4;
  optional uint32 data_parallel_start_rank = 5;
}
```

Revision `1` is the schema in this repository. Every server must populate:

- `schema_revision` with the exact monotonically increasing contract revision it
  implements. Zero is invalid.
- `minimum_client_revision` with the oldest client revision the server supports.
  A client below this revision must reject the server as incompatible.
- `schema_release` with an immutable OpenEngine repository release or source tag
  containing that revision. Moving branch names such as `main` are not valid.

Servers implementing this contract advertise `schema_revision = 1` and
`minimum_client_revision = 1`.

Clients should also define the oldest server revision they support and fail
closed when the advertised revision or release is outside their tested
compatibility range. This makes schema drift visible even while the package
name remains `openengine.v1`.

Discovery response scalars use proto3 `optional` presence. An absent value means
the engine cannot report the value; an explicitly present zero or `false` is a
reported value and must not be replaced with an orchestrator default.

Role semantics:

- `AGGREGATED`: accepts normal generation requests and returns tokens.  
- `PREFILL`: accepts prefill requests, builds KV state, emits handoff/session readiness, and does not perform normal decode generation.  
- `DECODE`: accepts decode requests with KV session/handoff metadata and returns generated tokens.  
- Engines must validate role/request compatibility before acceptance and return a
  non-OK gRPC status on mismatch.

---

## Model and capacity metadata

```protobuf
message GetModelInfoRequest {
  string model = 1;
}

message ModelInfo {
  string model_id = 1;
  string served_model_name = 2;
  repeated string served_model_aliases = 3;
  optional uint32 max_context_length = 4;
  optional uint32 max_output_tokens = 5;
  optional uint32 kv_block_size = 6;
  optional uint64 total_kv_blocks = 7;
  optional uint64 max_running_requests = 8;
  optional uint64 max_batched_tokens = 9;
  repeated string tokenizer_modes = 10;

  optional bool supports_text_input = 20;
  optional bool supports_token_ids_input = 21;
  GenerationCapabilities generation = 22;
  optional bool supports_lora = 23;
  optional bool supports_multimodal = 24;

  string reasoning_parser = 25;
  string tool_call_parser = 26;
}

message GenerationCapabilities {
  LogprobCapabilities prompt_logprobs = 1;
  LogprobCapabilities output_logprobs = 2;
  GuidedDecodingCapabilities guided_decoding = 3;
  optional uint32 max_num_sequences = 4;
  optional bool supports_priority = 5;
  optional bool supports_stop_in_output = 6;
  optional bool supports_cache_salt = 7;
  optional bool supports_prefix_cache_bypass = 8;
}

message LogprobCapabilities {
  optional bool supported = 1;
  repeated CandidateTokenSelectionMode candidate_selection_modes = 2;
  optional uint32 max_top_n = 3;
}

enum CandidateTokenSelectionMode {
  CANDIDATE_TOKEN_SELECTION_MODE_UNSPECIFIED = 0;
  CANDIDATE_TOKEN_SELECTION_MODE_TOP_N = 1;
  CANDIDATE_TOKEN_SELECTION_MODE_TOKEN_IDS = 2;
  CANDIDATE_TOKEN_SELECTION_MODE_ALL = 3;
}

message GuidedDecodingCapabilities {
  optional bool supported = 1;
  repeated GuidedDecodingMode modes = 2;
}

enum GuidedDecodingMode {
  GUIDED_DECODING_MODE_UNSPECIFIED = 0;
  GUIDED_DECODING_MODE_JSON_SCHEMA = 1;
  GUIDED_DECODING_MODE_REGEX = 2;
  GUIDED_DECODING_MODE_EBNF_GRAMMAR = 3;
  GUIDED_DECODING_MODE_STRUCTURAL_TAG = 4;
  GUIDED_DECODING_MODE_CHOICE = 5;
  GUIDED_DECODING_MODE_JSON_OBJECT = 6;
}
```

`GetModelInfoRequest.model` is required and selects one of
`EngineInfo.supported_models`; an unknown model returns gRPC `NOT_FOUND`.
Capability submessages distinguish unreported support (message absent) from
reported support or lack of support (`supported = true` or `false`). Candidate
selection modes and `max_top_n` are reported independently for prompt and
output logprobs. The remaining generation fields advertise support and limits
for the corresponding request options.

`supports_lora=true` means the engine accepts `GenerateRequest.lora_name` and
the LoRA lifecycle RPCs on `OpenEngine`.

---

## LoRA lifecycle

```protobuf
message LoraAdapter {
  int64 lora_id = 1;
  string lora_name = 2;
  string source_path = 3;
}

message LoadLoraRequest {
  LoraAdapter adapter = 1;
}

message LoadLoraResponse {
  LoraAdapter adapter = 1;
  bool already_loaded = 2;
}

message UnloadLoraRequest {
  string lora_name = 1;
}

message UnloadLoraResponse {
  LoraAdapter adapter = 1;
}

message ListLorasRequest {}

message ListLorasResponse {
  repeated LoraAdapter adapters = 1;
}
```

- `lora_id` must be positive.
- `lora_name` must be non-empty.
- `source_path` must be an absolute directory visible to the engine.
- Loading the same ID, name, and path twice is idempotent.
- A conflicting ID, name, or path returns `ALREADY_EXISTS`.
- An unknown adapter returns `NOT_FOUND`.
- A LoRA-disabled engine returns `FAILED_PRECONDITION`.

---

## Generation API

Generation is the core runtime completion primitive. Frontends or gateways may lower OpenAI chat-completion requests into this shape after applying chat templates and tokenization.

```protobuf
message GenerateRequest {
  string request_id = 1;
  string model = 2;

  oneof input {
    string prompt = 3;
    TokenIds token_ids = 4;
  }

  SamplingParams sampling = 5;
  StoppingOptions stopping = 6;
  ResponseOptions response = 7;
  KvOptions kv = 8;
  GuidedDecoding guided = 9;

  repeated MediaItem media = 10;
  string lora_name = 11;
  optional int32 priority = 12;
  map<string, string> metadata = 13;
}

message TokenIds {
  repeated uint32 ids = 1;
}

message SamplingParams {
  optional double temperature = 1;
  optional double top_p = 2;
  optional int32 top_k = 3;
  optional double min_p = 4;
  optional double frequency_penalty = 5;
  optional double presence_penalty = 6;
  optional double repetition_penalty = 7;
  optional uint64 seed = 8;
  optional uint32 num_sequences = 9;
}

message StoppingOptions {
  optional uint32 max_tokens = 1;
  optional uint32 min_tokens = 2;
  repeated StopCondition conditions = 3;
  optional bool ignore_eos = 4;
  optional bool include_stop_in_output = 5;
}

message ResponseOptions {
  optional bool return_prompt_logprobs = 1;
  CandidateTokenSelection prompt_candidates = 2;
  optional bool return_output_logprobs = 3;
  CandidateTokenSelection output_candidates = 4;
  optional uint32 prompt_logprob_start = 5;
}

message CandidateTokenSelection {
  oneof selection {
    uint32 top_n = 1;
    TokenIds token_ids = 2;
    AllCandidates all = 3;
  }
}

message AllCandidates {}

message KvOptions {
  KvSessionRef session = 1;
  optional uint32 data_parallel_rank = 2;
  optional bool bypass_prefix_cache = 3;
  optional string cache_salt = 4;
}

message StopCondition {
  oneof condition {
    string stop_text = 1;
    uint32 stop_token_id = 2;
  }
}

// Multimodal modality discriminator. 0 is treated as image for forward
// compatibility with senders that omit the field.
enum Modality {
  MODALITY_UNSPECIFIED = 0;
  MODALITY_IMAGE = 1;
  MODALITY_VIDEO = 2;
  MODALITY_AUDIO = 3;
}

// A single multimodal input. Exactly one `source` should be set. The engine
// owns fetch/decode/preprocess -- in the sidecar deployment the orchestrator
// has no GPU/NIXL agent, so a pre-decoded/RDMA media descriptor is NOT
// representable here by design.
message MediaItem {
  Modality modality = 1;
  oneof source {
    string url       = 2;   // http(s):// -- engine fetches
    string data_uri  = 3;   // data:<mime>;base64,<...> -- engine decodes
    bytes  raw_bytes = 4;   // pre-fetched bytes -- engine still preprocesses
  }
  string mime_type = 5;     // optional, hints raw_bytes decode
  string uuid      = 6;     // optional caller id / mm_hash
}

message GuidedDecoding {
  oneof guide {
    string json_schema = 1;
    string regex = 2;
    string ebnf_grammar = 3;
    string structural_tag = 4;
    ChoiceConstraint choice = 5;
    JsonObjectConstraint json_object = 6;
  }
  string backend = 7;
}

message ChoiceConstraint {
  repeated string choices = 1;
}

message JsonObjectConstraint {}
```

`SamplingParams` follows native engine sampling APIs, while stopping, returned
data, and KV/cache behavior remain separate option groups. Guided decoding stays
top-level as a distinct structured-output mode. Optional scalars preserve the
distinction between an engine default and explicit zero or `false`.

`priority` uses higher values for higher scheduling priority. `num_sequences`
defaults to one when omitted and must be greater than zero when present.
`CandidateTokenSelection` requests either the top N candidates, explicit token
IDs, or the full vocabulary at each prompt or output position. Select all
candidates with `all {}` and JSON-object guidance with `json_object {}`.

`Generate` is always a server-streaming RPC, so response options do not carry a
second streaming switch.

`include_stop_in_output` controls whether a matched caller-supplied stop token
or string remains in emitted output. `bypass_prefix_cache = true` skips prefix
cache reuse but does not prevent newly computed blocks from being cached.
`cache_salt` namespaces the prefix-cache key.

```protobuf
message GenerateResponse {
  string request_id = 1;

  oneof event {
    PromptOutput prompt = 2;
    TokenOutput token = 3;
    PrefillReady prefill_ready = 4;
    GenerationFinished finished = 5;
    EngineError error = 6;
  }

  Usage usage = 10;
}

message PromptOutput {
  repeated TokenInfo tokens = 1;
}

message TokenOutput {
  optional uint32 output_index = 1;
  repeated TokenInfo tokens = 2;
  string text = 3;
}

message TokenInfo {
  uint32 token_id = 1;
  string token = 2;
  optional double logprob = 3;
  optional uint32 rank = 4;
  repeated LogProb candidates = 5;
}

message LogProb {
  uint32 token_id = 1;
  double logprob = 2;
  string token = 3;
  optional uint32 rank = 4;
}

message PrefillReady {
  KvSessionRef kv_session = 1;
}

message GenerationFinished {
  optional uint32 output_index = 1;
  FinishReason reason = 2;
  string message = 3;
  StopMatch stop_match = 4;
}

message StopMatch {
  oneof match {
    uint32 stop_token_id = 1;
    string stop_text = 2;
    uint32 eos_token_id = 3;
  }
}

enum FinishReason {
  FINISH_REASON_UNSPECIFIED = 0;
  FINISH_REASON_STOP = 1;
  FINISH_REASON_LENGTH = 2;
  FINISH_REASON_CANCELLED = 3;
}

message Usage {
  uint32 prompt_tokens = 1;
  uint32 completion_tokens = 2;
  uint32 total_tokens = 3;
  optional uint32 cached_prompt_tokens = 4;
  optional uint32 reasoning_tokens = 5;
}
```

`PromptOutput` and `PrefillReady` are request-scoped. `TokenOutput` and
`GenerationFinished` are output-scoped and must carry `output_index`, including
index zero. An index is stable for the request and ranges from `0` through
`num_sequences - 1`.

`PromptOutput` is emitted at most once when prompt token information is
requested. Each prompt or output token is represented by one `TokenInfo`, so
its ID, text, score, rank, and candidates cannot become positionally
misaligned. The first prompt token has no conditional probability and therefore
omits `logprob` and `rank` and has no candidates. Candidate entries for other
tokens follow the corresponding prompt or output candidate selection.

Every `TokenOutput` contains only newly emitted token records and detokenized
text; neither field is cumulative. After `GenerationFinished` for an index, the
engine must not emit another token or terminal event for that index. A
successful aggregated or decode request emits exactly one
`GenerationFinished` for each requested output. `PrefillReady` is the terminal
success event for a prefill-only request.

`EngineError` is request-scoped and terminal. It terminates all outputs and may
replace `GenerationFinished` for outputs that had not completed. No event may
follow it. `Usage` is cumulative across every output in the request and is set
only on the final response, which is the last `GenerationFinished`,
`PrefillReady`, or the terminal `EngineError`.

When `FinishReason` is `STOP`, `stop_match` identifies the matched caller stop
token, stop string, or model EOS token. `cached_prompt_tokens` is a subset of
`prompt_tokens`; `reasoning_tokens` is a subset of `completion_tokens`.

---

## Disaggregated serving and KV API

The core API makes prefill/decode handoff explicit through
`GenerateRequest.kv.session` and `PrefillReady`, while engines own KV transfer
mechanics and session lifetime.

```protobuf
message KvSessionRef {
  string session_id = 1;
  string transfer_backend = 2;
  repeated KvEndpoint endpoints = 3;
  uint32 dp_rank = 4;
  google.protobuf.Struct attributes_struct = 5; // type-preserving KV-transfer params
}

message KvEndpoint {
  string host = 1;
  uint32 port = 2;
  string protocol = 3; // grpc, nixl, ucx, tcp, shm, etc.
}

```

`attributes_struct` requires `import "google/protobuf/struct.proto";` at the
top of the proto.

`attributes_struct` preserves number, boolean, array, and object types. Struct
numbers are IEEE-754 doubles, so values above 2^53 should use strings or a
dedicated field.

Prefill flow:

1. Orchestrator sends `GenerateRequest` to a `PREFILL` engine.  
2. Engine returns a `KvSessionRef` in the terminal `PrefillReady` response when
   decode may attach.
3. Engine owns KV session lifetime and cleanup, including finish, abort, drain, timeout, and transfer failure paths.  
4. An accepted prefill failure produces one terminal `EngineError` instead.

Decode flow:

1. Orchestrator sends `GenerateRequest` to a `DECODE` engine with `kv.session` set.
2. Decode engine validates the session and transfer backend.  
3. Decode engine generates tokens.

---

## KV connector and KV events

OpenEngine should support two KV-event modes:

1. **Native OpenEngine stream:** `SubscribeKvEvents` returns envelopes containing
   typed protobuf batches.
2. **Compatibility source discovery:** `GetKvEventSources` advertises existing engine-native sources such as SGLang/vLLM ZMQ publishers.  
   

```protobuf
message GetKvConnectorInfoRequest {}

message KvConnectorInfo {
  optional bool enabled = 1;
  string transfer_backend = 2;
  repeated KvEndpoint local_endpoints = 3;
  repeated string supported_protocols = 4;
  optional bool supports_remote_prefill = 5;
  optional bool supports_decode_pull = 6;
  optional bool supports_abort_cleanup = 7;
  optional bool supports_drain = 8;
  optional uint32 schema_version = 9;
}

message GetKvEventSourcesRequest {
  repeated uint32 data_parallel_ranks = 1;
}

message GetKvEventSourcesResponse {
  repeated KvEventSource sources = 1;
}

message KvEventSource {
  string transport = 1;          // grpc, zmq
  KvEndpoint endpoint_addr = 2; // connectable host:port, never a bind wildcard
  string topic = 3;
  string replay_endpoint = 4;    // optional, for ZMQ replay
  optional uint32 data_parallel_rank = 5;
  string encoding = 6;           // protobuf, msgpack
  optional uint32 schema_version = 7;
  optional uint32 buffer_steps = 8;
  optional uint32 hwm = 9;
  optional uint32 max_queue_size = 10;
}

message SubscribeKvEventsRequest {
  repeated uint32 data_parallel_ranks = 1;
  bool include_snapshot = 2;
  uint64 start_sequence_number = 3;
}

message SubscribeKvEventsResponse {
  oneof event {
    KvEventBatch batch = 1;
    EngineError error = 2;
  }
}

message KvEventBatch {
  uint64 sequence_number = 1;
  uint64 timestamp_unix_nanos = 2;
  uint32 data_parallel_rank = 3;
  repeated KvEvent events = 4;
}

message KvEvent {
  string request_id = 1;
  KvSessionRef kv_session = 2;

  oneof event {
    BlockStored block_stored = 10;
    BlockRemoved block_removed = 11;
    AllBlocksCleared all_blocks_cleared = 12;
  }
}

message BlockStored {
  repeated KvBlockHash block_hashes = 1;
  KvBlockHash parent_block_hash = 2;
  repeated uint32 token_ids = 3;
  uint32 block_size = 4;
  int64 lora_id = 5;
  string lora_name = 6;
  StorageMedium medium = 7;

  // vLLM-compatible optional metadata for reconstructing block keys.
  repeated OpaqueKeyTuple extra_keys = 20;
  uint32 group_idx = 21;
  string kv_cache_spec_kind = 22;
  uint32 kv_cache_spec_sliding_window = 23;
}

message BlockRemoved {
  repeated KvBlockHash block_hashes = 1;
  StorageMedium medium = 2;
  uint32 group_idx = 3;
}

message AllBlocksCleared {}

message KvBlockHash {
  bytes value = 1;
  string encoding = 2; // int64, string, bytes, engine_specific
}

message OpaqueKeyTuple {
  repeated string values = 1;
}

enum StorageMedium {
  STORAGE_MEDIUM_UNSPECIFIED = 0;
  STORAGE_MEDIUM_GPU = 1;
  STORAGE_MEDIUM_CPU_PINNED = 2;
  STORAGE_MEDIUM_DISK = 3;
  STORAGE_MEDIUM_EXTERNAL = 4;
}
```

Compatibility notes:

- SGLang/vLLM-style `BlockStored`, `BlockRemoved`, and `AllBlocksCleared` are first-class OpenEngine events.  
- OpenEngine preserves batch timestamp, DP-rank attribution, monotonic sequence numbers, replay start sequence, topic, endpoint, replay endpoint, buffer size, HWM, and queue-size metadata.  
- Native OpenEngine streams should use protobuf. Existing ZMQ/msgpack publishers can be exposed through `GetKvEventSources` during migration.  
- Orchestrators should prefer `SubscribeKvEvents` when available and fall back to engine-native sources when advertised.  
- `endpoint_addr` MUST carry a routable `host:port`, never a bind wildcard such
  as `*` or `0.0.0.0`.

After subscription acceptance, an application failure is the final
`SubscribeKvEventsResponse` with `error` set. No batch may follow it, and the
server closes the stream with gRPC `OK`.

---

## Health, abort, and drain

```protobuf
message HealthRequest {
  // False means a lightweight readiness/liveness check. True asks the engine to
  // run a role-appropriate minimal inference probe and report it as a check.
  bool include_inference_probe = 1;

  // Optional. Used when include_inference_probe is true. Empty means engine
  // default served model.
  string model = 2;

  // Optional expected role for role-specific inference probes.
  EngineRole role = 3;
}

message HealthResponse {
  HealthState state = 1;
  repeated HealthCheck checks = 2;
}

enum HealthState {
  HEALTH_STATE_UNSPECIFIED = 0;
  HEALTH_STATE_STARTING = 1;
  HEALTH_STATE_READY = 2;
  HEALTH_STATE_DEGRADED = 3;
  HEALTH_STATE_DRAINING = 4;
  HEALTH_STATE_NOT_READY = 5;
}

message HealthCheck {
  string name = 1; // grpc, scheduler, model, kv_connector, role, inference_probe
  HealthState state = 2;
  string message = 3;
}

message AbortRequest {
  oneof target {
    string request_id = 1;
    KvSessionRef kv_session = 2;
    AllRequests all_requests = 3;
  }
}

message AllRequests {}

message AbortResponse {
  AbortStatus status = 1;
  string message = 2;
}

enum AbortStatus {
  ABORT_STATUS_UNSPECIFIED = 0;
  ABORT_STATUS_ABORTED = 1;
  ABORT_STATUS_ALREADY_FINISHED = 2;
}

message DrainRequest {
  bool stop_accepting_new_requests = 1;
  optional uint32 deadline_ms = 2;
  bool abort_after_deadline = 3;
}

message DrainResponse {
  oneof event {
    DrainState state = 1;
    EngineError error = 5;
  }
  optional uint32 in_flight_requests = 2;
  optional uint32 open_kv_sessions = 3;
  string message = 4;
}

enum DrainState {
  DRAIN_STATE_UNSPECIFIED = 0;
  DRAIN_STATE_STARTED = 1;
  DRAIN_STATE_IN_PROGRESS = 2;
  DRAIN_STATE_COMPLETE = 3;
}
```

Exactly one abort target must be set. Use `all_requests {}` to abort every
request; omitting the target returns gRPC `INVALID_ARGUMENT`. An unknown request
or KV session target returns gRPC `NOT_FOUND`; an engine that does not support
abort returns gRPC `UNIMPLEMENTED`. `ALREADY_FINISHED` remains a successful
idempotent outcome rather than an error.

`STARTED` and `IN_PROGRESS` are progress events; `COMPLETE` is terminal. A
failure after the drain is accepted is represented by one terminal
`EngineError`, not by a failed drain state. An absent `deadline_ms` means no
deadline; an explicit zero means the deadline is immediate. Absent progress
counts are unknown, while present zero values report that no requests or KV
sessions remain.

---

## Runtime observability

`GetLoad` returns a structured point-in-time load snapshot for schedulers and admission controllers. It is not a replacement for Prometheus metrics; it is the engine-facing control-plane signal for request routing and overload decisions.

```protobuf
message GetLoadRequest {
  bool include_per_rank = 1;
}

message LoadInfo {
  string instance_id = 1;
  optional uint64 timestamp_unix_nanos = 2;
  optional uint32 running_requests = 3;
  optional uint32 queued_requests = 4;
  optional uint32 active_kv_sessions = 5;
  optional uint64 used_kv_blocks = 6;
  optional uint64 total_kv_blocks = 7;
  optional uint64 running_tokens = 8;
  optional uint64 waiting_tokens = 9;
  optional uint32 prefill_batch_size = 10;
  optional uint32 decode_batch_size = 11;
  repeated RankLoadInfo ranks = 20;
  map<string, string> attributes = 30;
}

message RankLoadInfo {
  optional uint32 data_parallel_rank = 1;
  optional uint32 running_requests = 2;
  optional uint32 queued_requests = 3;
  optional uint64 used_kv_blocks = 4;
  optional uint64 total_kv_blocks = 5;
  optional uint32 prefill_batch_size = 6;
  optional uint32 decode_batch_size = 7;
}
```

Every load scalar has explicit presence. Absent means unavailable in that
engine or snapshot; present zero means the measured load is zero.

Runtime event stream:

```protobuf
message SubscribeRuntimeEventsRequest {
  repeated RuntimeEventType types = 1;
}

message SubscribeRuntimeEventsResponse {
  oneof event {
    RuntimeEvent runtime_event = 1;
    EngineError error = 2;
  }
}

enum RuntimeEventType {
  RUNTIME_EVENT_TYPE_UNSPECIFIED = 0;
  RUNTIME_EVENT_TYPE_FORWARD_PASS = 1;
  RUNTIME_EVENT_TYPE_BATCH = 2;
  RUNTIME_EVENT_TYPE_QUEUE = 3;
  RUNTIME_EVENT_TYPE_TRANSFER = 4;
}

message RuntimeEvent {
  string event_id = 1;
  uint64 timestamp_unix_nanos = 2;
  RuntimeEventType type = 3;
  map<string, string> attributes = 4;
}
```

After subscription acceptance, an application failure is the final
`SubscribeRuntimeEventsResponse` with `error` set. No runtime event may follow
it, and the server closes the stream with gRPC `OK`.

---

## Standard errors

```protobuf
message EngineError {
  ErrorCode code = 1;
  string message = 2;
  bool retryable = 3;
  optional uint64 retry_after_ms = 4;
  google.protobuf.Struct details = 5;
}

enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_INVALID_ARGUMENT = 1;
  ERROR_CODE_UNSUPPORTED_FEATURE = 2;
  ERROR_CODE_ROLE_MISMATCH = 3;
  ERROR_CODE_MODEL_NOT_FOUND = 4;
  ERROR_CODE_OVERLOADED = 5;
  ERROR_CODE_REQUEST_NOT_FOUND = 6;
  ERROR_CODE_DUPLICATE_REQUEST = 7;
  ERROR_CODE_KV_SESSION_NOT_FOUND = 8;
  ERROR_CODE_KV_TRANSFER_FAILED = 9;
  ERROR_CODE_CANCELLED = 10;
  ERROR_CODE_DRAINING = 11;
  ERROR_CODE_INTERNAL = 12;
}
```

Errors have exactly one transport based on when and where they occur:

| Phase | Representation | Stream termination |
|---|---|---|
| Before request acceptance | Non-OK gRPC status | No response event |
| Accepted request, application failure | Exactly one terminal `EngineError` event | gRPC `OK` after the event |
| Transport or gRPC framework failure | Non-OK gRPC status | No synthesized `EngineError` |

Acceptance is the boundary after synchronous validation and admission succeed
and the server commits the operation for execution. Unary RPCs have no separate
accepted stream phase and report failures with non-OK gRPC status.

`GenerationFinished` is terminal for its `output_index`; other output indexes
may continue. The last `GenerationFinished` ends a successful aggregated or
decode stream, `PrefillReady` ends a successful prefill stream, and
`EngineError` ends any failed generation stream. `DrainState.COMPLETE` and
`EngineError` terminate a drain stream. An `EngineError` also terminates a
KV-event or runtime-event subscription. No response may follow a terminal
`EngineError`. Application failure is neither a `GenerationFinished` reason nor
a failed drain state.

`retryable` states whether the unchanged operation can succeed on retry.
`retry_after_ms` is present only for retryable errors and is the recommended
minimum delay; an explicit zero permits immediate retry. `details` contains
machine-readable error context. Stable detail keys are part of this API;
engine-specific keys should be namespaced to avoid collisions.
