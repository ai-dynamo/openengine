use std::env;
use std::fs;
use std::path::Path;

use openengine_proto::openengine::v1::{
    generate_request, media_item, GenerateRequest, KvBootstrap, KvEndpoint, KvOptions,
    KvSessionRef, MediaItem, Modality,
};
use prost::Message;
use prost_types::{value, Struct, Value};

fn number(value: f64) -> Value {
    Value {
        kind: Some(value::Kind::NumberValue(value)),
    }
}

fn boolean(value: bool) -> Value {
    Value {
        kind: Some(value::Kind::BoolValue(value)),
    }
}

fn string(value: impl Into<String>) -> Value {
    Value {
        kind: Some(value::Kind::StringValue(value.into())),
    }
}

fn structure(fields: impl IntoIterator<Item = (&'static str, Value)>) -> Struct {
    Struct {
        fields: fields
            .into_iter()
            .map(|(key, value)| (key.to_owned(), value))
            .collect(),
    }
}

fn media_options() -> Struct {
    structure([
        (
            "image",
            Value {
                kind: Some(value::Kind::StructValue(structure([
                    ("min_pixels", number(3136.0)),
                    ("do_resize", boolean(true)),
                ]))),
            },
        ),
        (
            "video",
            Value {
                kind: Some(value::Kind::StructValue(structure([(
                    "max_frames",
                    number(8.0),
                )]))),
            },
        ),
    ])
}

fn kv_session(profile: &str) -> KvSessionRef {
    let endpoint = KvEndpoint {
        host: "decode.internal".into(),
        port: 24000,
        protocol: "tcp".into(),
    };
    let attributes_struct = match profile {
        "tensorrt_llm.disaggregated_params.v1" => structure([(
            "tensorrt_llm.disaggregated_params.v1",
            string(r#"{"ctx_request_id":"18446744073709551614","opaque_state":"AP8="}"#),
        )]),
        "vllm.kv_transfer_params.v1" => structure([
            ("request_id", string("18446744073709551614")),
            ("opaque_state", string("AP8=")),
        ]),
        "sglang.bootstrap.v1" => structure([
            ("bootstrap_owner", string("client")),
            ("opaque_state", string("AP8=")),
        ]),
        _ => panic!("unknown handoff profile: {profile}"),
    };
    let bootstrap = (profile == "sglang.bootstrap.v1").then(|| KvBootstrap {
        endpoint: Some(endpoint.clone()),
        room_id: 18_446_744_073_709_551_614,
    });

    KvSessionRef {
        session_id: "cross-language-session".into(),
        transfer_backend: "fixture".into(),
        endpoints: vec![endpoint],
        dp_rank: 7,
        attributes_struct: Some(attributes_struct),
        handoff_profile: profile.into(),
        bootstrap,
    }
}

fn fixture(profile: &str) -> GenerateRequest {
    GenerateRequest {
        request_id: "cross-language".into(),
        model: "test-model".into(),
        input: Some(generate_request::Input::Prompt("Hello".into())),
        media: vec![
            MediaItem {
                modality: Modality::Image as i32,
                source: Some(media_item::Source::RawBytes(vec![0, 1, 255])),
                mime_type: "image/png".into(),
                uuid: "image-0".into(),
            },
            MediaItem {
                modality: Modality::Video as i32,
                source: Some(media_item::Source::Url(
                    "https://example.invalid/video.mp4".into(),
                )),
                uuid: "video-1".into(),
                ..Default::default()
            },
        ],
        media_options: Some(media_options()),
        kv: Some(KvOptions {
            session: Some(kv_session(profile)),
            ..Default::default()
        }),
        ..Default::default()
    }
}

fn encode(profile: &str, path: &Path) {
    fs::write(path, fixture(profile).encode_to_vec()).unwrap();
}

fn decode(profile: &str, path: &Path) {
    let bytes = fs::read(path).unwrap();
    let request = GenerateRequest::decode(bytes.as_slice()).unwrap();
    assert_eq!(request, fixture(profile));
}

fn main() {
    let mut args = env::args_os().skip(1);
    let operation = args.next().expect("expected encode or decode");
    let profile = args.next().expect("expected handoff profile");
    let path = args.next().expect("expected fixture path");
    assert!(args.next().is_none(), "unexpected additional arguments");
    let profile = profile.to_str().expect("handoff profile must be UTF-8");

    match operation.to_str() {
        Some("encode") => encode(profile, Path::new(&path)),
        Some("decode") => decode(profile, Path::new(&path)),
        _ => panic!("expected encode or decode"),
    }
}
