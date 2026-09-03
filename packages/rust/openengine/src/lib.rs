//! Generated Prost messages and Tonic services for OpenEngine.

// Protobuf comments may contain angle-bracket metavariables that rustdoc
// otherwise interprets as HTML tags.
#![allow(rustdoc::invalid_html_tags)]

/// Monotonically increasing revision of the packaged wire contract.
pub const SCHEMA_REVISION: u32 = 1;

/// Immutable Buf Schema Registry commit corresponding to these bindings.
pub const SCHEMA_RELEASE: &str = "768a93c7b44e40f28c692ad0b471a8f2";

/// Serialized descriptors for the complete `openengine.v1` package.
pub const FILE_DESCRIPTOR_SET: &[u8] = include_bytes!("generated/openengine_descriptor.bin");

/// Version 1 of the OpenEngine wire API.
pub mod v1 {
    include!("generated/openengine.v1.rs");
}
