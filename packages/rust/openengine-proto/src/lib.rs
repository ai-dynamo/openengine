//! Generated Prost messages and Tonic services for OpenEngine.

/// Monotonically increasing revision of the packaged wire contract.
pub const SCHEMA_REVISION: u32 = 1;

/// Immutable OpenEngine release corresponding to these bindings.
pub const SCHEMA_RELEASE: &str = concat!("v", env!("CARGO_PKG_VERSION"));

/// Serialized descriptors for the complete `openengine.v1` package.
pub const FILE_DESCRIPTOR_SET: &[u8] = include_bytes!("generated/openengine_descriptor.bin");

/// Modules arranged to match the protobuf package name.
pub mod openengine {
    /// Version 1 of the OpenEngine wire API.
    pub mod v1 {
        include!("generated/openengine.v1.rs");
    }
}
