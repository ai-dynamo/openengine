use openengine_proto::openengine::v1::{generate_request, GenerateRequest, SamplingParams};
use openengine_proto::{
    FILE_DESCRIPTOR_SET, MINIMUM_CLIENT_REVISION, SCHEMA_RELEASE, SCHEMA_REVISION,
};
use prost::Message;
use prost_types::FileDescriptorSet;

#[test]
fn request_round_trip_preserves_optional_zero() {
    let request = GenerateRequest {
        request_id: "rust-smoke".into(),
        model: "test-model".into(),
        input: Some(generate_request::Input::Prompt("Hello".into())),
        sampling: Some(SamplingParams {
            temperature: Some(0.0),
            ..Default::default()
        }),
        ..Default::default()
    };

    let decoded = GenerateRequest::decode(request.encode_to_vec().as_slice()).unwrap();

    assert_eq!(decoded.request_id, "rust-smoke");
    assert_eq!(decoded.sampling.unwrap().temperature, Some(0.0));
    assert!(matches!(
        decoded.input,
        Some(generate_request::Input::Prompt(prompt)) if prompt == "Hello"
    ));
}

#[test]
fn descriptor_set_contains_inference_and_control_services() {
    let descriptors = FileDescriptorSet::decode(FILE_DESCRIPTOR_SET).unwrap();
    let service_file = descriptors
        .file
        .iter()
        .find(|file| file.name.as_deref() == Some("openengine/v1/openengine.proto"))
        .unwrap();

    assert!(service_file
        .service
        .iter()
        .any(|service| service.name.as_deref() == Some("Inference")));

    let inference = service_file
        .service
        .iter()
        .find(|service| service.name.as_deref() == Some("Inference"))
        .unwrap();
    assert_eq!(
        inference
            .method
            .iter()
            .filter_map(|method| method.name.as_deref())
            .collect::<Vec<_>>(),
        ["Generate"]
    );
    let control = service_file
        .service
        .iter()
        .find(|service| service.name.as_deref() == Some("Control"))
        .unwrap();
    assert!(control
        .method
        .iter()
        .any(|method| method.name.as_deref() == Some("GetServerInfo")));
    assert!(!control
        .method
        .iter()
        .any(|method| method.name.as_deref() == Some("SubscribeRuntimeEvents")));
}

#[test]
fn descriptor_set_contains_revision_2_multimodal_fields() {
    let descriptors = FileDescriptorSet::decode(FILE_DESCRIPTOR_SET).unwrap();
    let find_message = |name: &str| {
        descriptors
            .file
            .iter()
            .flat_map(|file| file.message_type.iter())
            .find(|message| message.name.as_deref() == Some(name))
            .unwrap()
    };

    let generate_request = find_message("GenerateRequest");
    let media_options = generate_request
        .field
        .iter()
        .find(|field| field.name.as_deref() == Some("media_options"))
        .unwrap();
    assert_eq!(media_options.number, Some(14));
    assert_eq!(
        media_options.type_name.as_deref(),
        Some(".google.protobuf.Struct")
    );

    let model_info = find_message("ModelInfo");
    let capabilities = model_info
        .field
        .iter()
        .find(|field| field.name.as_deref() == Some("multimodal_capabilities"))
        .unwrap();
    assert_eq!(capabilities.number, Some(29));
    assert_eq!(
        capabilities.type_name.as_deref(),
        Some(".openengine.v1.MultimodalCapabilities")
    );
}

#[test]
fn descriptor_set_contains_revision_3_discovery_and_handoff_fields() {
    fn field<'a>(
        message: &'a prost_types::DescriptorProto,
        name: &str,
    ) -> &'a prost_types::FieldDescriptorProto {
        message
            .field
            .iter()
            .find(|field| field.name.as_deref() == Some(name))
            .unwrap()
    }

    let descriptors = FileDescriptorSet::decode(FILE_DESCRIPTOR_SET).unwrap();
    let find_message = |name: &str| {
        descriptors
            .file
            .iter()
            .flat_map(|file| file.message_type.iter())
            .find(|message| message.name.as_deref() == Some(name))
            .unwrap()
    };
    let model_info = find_message("ModelInfo");
    let tokenizer = field(model_info, "tokenizer");
    assert_eq!(tokenizer.number, Some(11));
    assert_eq!(
        tokenizer.type_name.as_deref(),
        Some(".openengine.v1.TokenizerInfo")
    );

    let multimodal = find_message("MultimodalCapabilities");
    let routing_token = field(multimodal, "routing_image_token_id");
    assert_eq!(routing_token.number, Some(5));
    assert_eq!(routing_token.proto3_optional, Some(true));

    let session = find_message("KvSessionRef");
    assert_eq!(field(session, "handoff_profile").number, Some(6));
    let bootstrap = field(session, "bootstrap");
    assert_eq!(bootstrap.number, Some(7));
    assert_eq!(
        bootstrap.type_name.as_deref(),
        Some(".openengine.v1.KvBootstrap")
    );

    let bootstrap = find_message("KvBootstrap");
    assert_eq!(field(bootstrap, "endpoint").number, Some(1));
    assert_eq!(field(bootstrap, "room_id").number, Some(2));

    let connector = find_message("KvConnectorInfo");
    assert_eq!(field(connector, "handoff_profile").number, Some(10));
    let client_bootstrap = field(connector, "supports_client_bootstrap");
    assert_eq!(client_bootstrap.number, Some(11));
    assert_eq!(client_bootstrap.proto3_optional, Some(true));
}

#[test]
fn package_metadata_matches_schema() {
    assert_eq!(SCHEMA_REVISION, 3);
    assert_eq!(MINIMUM_CLIENT_REVISION, 1);
    assert_eq!(SCHEMA_RELEASE, "unreleased");
}
