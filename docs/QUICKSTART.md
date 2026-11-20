<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0
-->

# Using OpenEngine

Send text or token IDs to an engine and read the output as a stream. The [API reference](api.md) and [Protobuf schema](../proto/openengine/v1/) cover multimodal input, LoRA, guided decoding, logprobs, multiple outputs, and both KV event paths.

## 1. Discover the engine and model

1. Call `Control.GetServerInfo` to identify the engine and check schema compatibility. Choose a model from `ServerInfo.supported_models`.
2. Pass that name in `GetModelInfoRequest.model` when calling `Control.GetModelInfo`. For example, if the list contains `my-model`, send `{"model": "my-model"}`. The response lists the model's limits and supported features.
3. Use the returned `ModelInfo.served_model_name` or one of its `served_model_aliases` as `GenerateRequest.model`.

An omitted optional discovery field means the engine has not reported a value. An explicit `false` means unsupported. For request options, an omitted optional scalar uses the engine or model default. See the [presence and compatibility rules](api.md#server-identity-deployment-capacity-and-engine-roles).

## 2. Send a basic request

This protobuf-JSON request allows up to 64 output tokens:

```json
{
  "requestId": "request-1",
  "model": "my-model",
  "prompt": "Explain continuous batching.",
  "stopping": { "maxTokens": 64 }
}
```

Replace `my-model` with the served model. Set exactly one of `prompt` and `token_ids`. The request ID identifies the operation in streamed responses and control calls.

| Group | What belongs here | Omission |
| --- | --- | --- |
| `sampling` | Temperature, probability filters, penalties, seed, and number of sequences | Engine/model defaults; `num_sequences` defaults to one |
| `stopping` | Output budget, stop strings/tokens, and EOS/stop-output options | Engine defaults for unspecified values |
| `response` | Prompt/output logprobs, candidate selection, and prompt offset | No additional scoring is selected by a candidate selector alone |
| `guided` | JSON, regex, grammar, structural tags, or fixed choices | No requested output constraint; an empty backend selects the engine default |
| `media` | Ordered image/video/audio inputs with their source and identity | Text/token input without media |
| `lora_name` | A previously loaded adapter | Base model |
| `kv` | Handoff session and prefix-cache behavior | No supplied handoff; other cache policy stays engine-owned |
| `extra` | Documented, engine-specific extensions | The request remains valid without this best-effort extension |

Set optional scalars explicitly when their value matters. Preserve the distinction between omitted values and explicit zero or false when converting requests. See the [generation reference](api.md#generation-api) for validation and supported feature combinations.

## 3. Add multimodal input

Add an ordered `media` list alongside the prompt or token IDs. In this example, replace `<image>` with the loaded model's actual, unexpanded image placeholder before sending the request.

```json
{
  "requestId": "request-image-1",
  "model": "my-vision-model",
  "prompt": "<image> Describe this image.",
  "media": [
    {
      "modality": "MODALITY_IMAGE",
      "url": "https://example.com/image.png",
      "uuid": "image-1"
    }
  ],
  "stopping": { "maxTokens": 64 }
}
```

Use the deployment's model name and a real image URL. Match each media item to its corresponding placeholder, including when modalities are mixed. The engine fetches and decodes the media, preprocesses it, and expands the placeholders.

| Media field | Purpose |
| --- | --- |
| `modality` | Distinguishes image, video, and audio; support depends on the model and engine |
| `url`, `data_uri`, or `raw_bytes` | Exactly one source: URL, data URI, or raw bytes |
| `mime_type` | MIME hint for raw bytes |
| `uuid` | Optional caller identity passed through for native correlation/cache behavior |

A model reporting `supports_multimodal = true` supports at least one modality. The engine rejects unsupported modalities and source encodings. The [media contract](api.md#generation-api) accepts URLs, data URIs, and raw bytes, and preserves caller UUIDs.

## 4. Consume the stream

Each `GenerateResponse.event` carries prompt information, token deltas, prefill readiness, per-output completion, or request failure. Token text and records are incremental. Only the final response carries request-level usage.

For multiple sequences, track `TokenOutput.output_index` and `GenerationFinished.output_index` separately. Each sequence finishes independently; a request-level `EngineError` ends all remaining outputs. The [terminal-event rules](api.md#standard-errors) distinguish application errors from gRPC errors.

## 5. Use control and KV features when needed

| Need | Interface |
| --- | --- |
| Routine readiness/liveness | Standard `grpc.health.v1.Health`, with `readiness` and `liveness` |
| Detailed checks or inference probes | `Control.Health` |
| Configured deployment ceilings | `ServerInfo.capacity` |
| Current utilization | `Control.GetLoad`; request per-rank detail only when needed |
| Adapter management | `LoadLora`, `UnloadLora`, `ListLoras` |
| Cancellation or shutdown | `Abort`, or `Shutdown` with the engine instance ID |
| Prefill/decode | `PrefillReady.kv_session` forwarded to `GenerateRequest.kv.session` |
| Cache-aware routing | Typed `SubscribeKvEvents`, or `GetKvEventSources` for a native publisher |

When upgrading from v0.1.0, verify that the engine recognizes each named health probe before switching to it. To call `Shutdown`, use bindings that include the RPC and handle `UNIMPLEMENTED` from servers without shutdown support. See the [schema compatibility notes](../proto/openengine/v1/README.md).

The deployment's role and engine configuration determine the prefill/decode phase. Forward KV handoff attributes unchanged, including native endpoint and transfer state. Follow the [precision and binary encoding rules](api.md#disaggregated-serving-and-kv-api) for their typed-JSON representation.
