// SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

use openengine::FILE_DESCRIPTOR_SET;
use prost::Message;
use prost_types::FileDescriptorSet;

#[test]
fn descriptor_exposes_server_streaming_generate() {
    let descriptors = FileDescriptorSet::decode(FILE_DESCRIPTOR_SET).expect("valid descriptor set");
    let generate = descriptors
        .file
        .iter()
        .filter(|file| file.package() == "openengine.v1")
        .flat_map(|file| &file.service)
        .find(|service| service.name() == "Inference")
        .expect("openengine.v1.Inference service")
        .method
        .iter()
        .find(|method| method.name() == "Generate")
        .expect("Generate method");

    assert!(generate.server_streaming());
    assert!(!generate.client_streaming());
}
