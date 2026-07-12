//! Generated Prost messages and Tonic services for OpenEngine.

/// Monotonically increasing revision of the packaged wire contract.
pub const SCHEMA_REVISION: u32 = 2;

/// Oldest client schema revision compatible with this contract.
pub const MINIMUM_CLIENT_REVISION: u32 = 1;

/// Sentinel used until an engine injects its immutable OpenEngine commit or tag.
///
/// A package version cannot identify the source commit of a path or Git
/// dependency, so servers must not advertise this value as a release identity.
pub const SCHEMA_RELEASE: &str = "unreleased";

/// Serialized descriptors for the complete `openengine.v1` package.
pub const FILE_DESCRIPTOR_SET: &[u8] = include_bytes!("generated/openengine_descriptor.bin");

/// Modules arranged to match the protobuf package name.
pub mod openengine {
    /// Version 1 of the OpenEngine wire API.
    pub mod v1 {
        include!("generated/openengine.v1.rs");
    }
}
