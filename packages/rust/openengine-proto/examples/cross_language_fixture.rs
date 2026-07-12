use std::env;
use std::fs;
use std::path::Path;

use openengine_proto::openengine::v1::{
    generate_request, media_item, GenerateRequest, MediaItem, Modality,
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

fn fixture() -> GenerateRequest {
    GenerateRequest {
        request_id: "cross-language".into(),
        model: "test-model".into(),
        input: Some(generate_request::Input::Prompt("Hello".into())),
        priority: Some(0),
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
        ..Default::default()
    }
}

fn encode(path: &Path) {
    fs::write(path, fixture().encode_to_vec()).unwrap();
}

fn decode(path: &Path) {
    let bytes = fs::read(path).unwrap();
    let request = GenerateRequest::decode(bytes.as_slice()).unwrap();
    assert_eq!(request, fixture());
}

fn main() {
    let mut args = env::args_os().skip(1);
    let operation = args.next().expect("expected encode or decode");
    let path = args.next().expect("expected fixture path");
    assert!(args.next().is_none(), "unexpected additional arguments");

    match operation.to_str() {
        Some("encode") => encode(Path::new(&path)),
        Some("decode") => decode(Path::new(&path)),
        _ => panic!("expected encode or decode"),
    }
}
