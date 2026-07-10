use std::env;
use std::fs;
use std::path::Path;

use openengine_proto::openengine::v1::{generate_request, GenerateRequest};
use prost::Message;

fn fixture() -> GenerateRequest {
    GenerateRequest {
        request_id: "cross-language".into(),
        model: "test-model".into(),
        input: Some(generate_request::Input::Prompt("Hello".into())),
        priority: Some(0),
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
