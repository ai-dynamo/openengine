//! Generated Prost messages and Tonic services for OpenEngine.

// Protobuf comments may contain angle-bracket metavariables that rustdoc
// otherwise interprets as HTML tags.
#![allow(rustdoc::invalid_html_tags)]

include!("generated/schema.rs");

/// Serialized descriptors for the complete `openengine.v1` package.
pub const FILE_DESCRIPTOR_SET: &[u8] = include_bytes!("generated/openengine_descriptor.bin");

/// Version 1 of the OpenEngine wire API.
pub mod v1 {
    include!("generated/openengine.v1.rs");
}
