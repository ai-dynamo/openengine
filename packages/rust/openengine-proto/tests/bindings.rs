use openengine_proto::openengine::v1::{generate_request, GenerateRequest};
use openengine_proto::{FILE_DESCRIPTOR_SET, SCHEMA_RELEASE, SCHEMA_REVISION};
use prost::Message;
use prost_types::FileDescriptorSet;

#[test]
fn request_round_trip_preserves_optional_zero() {
    let request = GenerateRequest {
        request_id: "rust-smoke".into(),
        model: "test-model".into(),
        input: Some(generate_request::Input::Prompt("Hello".into())),
        priority: Some(0),
        ..Default::default()
    };

    let decoded = GenerateRequest::decode(request.encode_to_vec().as_slice()).unwrap();

    assert_eq!(decoded.request_id, "rust-smoke");
    assert_eq!(decoded.priority, Some(0));
    assert!(matches!(
        decoded.input,
        Some(generate_request::Input::Prompt(prompt)) if prompt == "Hello"
    ));
}

#[test]
fn descriptor_set_contains_openengine_service() {
    let descriptors = FileDescriptorSet::decode(FILE_DESCRIPTOR_SET).unwrap();
    let service_file = descriptors
        .file
        .iter()
        .find(|file| file.name.as_deref() == Some("openengine/v1/openengine.proto"))
        .unwrap();

    assert!(service_file
        .service
        .iter()
        .any(|service| service.name.as_deref() == Some("OpenEngine")));
}

#[test]
fn package_metadata_matches_schema() {
    assert_eq!(SCHEMA_REVISION, 1);
    assert_eq!(SCHEMA_RELEASE, concat!("v", env!("CARGO_PKG_VERSION")));
}
