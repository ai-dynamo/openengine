use std::env;
use std::error::Error;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn Error>> {
    let repository = env::args_os()
        .nth(1)
        .map(PathBuf::from)
        .unwrap_or(env::current_dir()?);
    let proto_root = repository.join("proto");
    let package_root = proto_root.join("openengine/v1");
    let output = repository.join("packages/rust/openengine-proto/src/generated");

    fs::create_dir_all(&output)?;

    let mut protos = fs::read_dir(&package_root)?
        .filter_map(Result::ok)
        .map(|entry| entry.path())
        .filter(|path| {
            path.extension()
                .is_some_and(|extension| extension == "proto")
        })
        .collect::<Vec<_>>();
    protos.sort();

    let protoc = protoc_bin_vendored::protoc_bin_path()?;
    let protobuf_include = protoc_bin_vendored::include_path()?;
    env::set_var("PROTOC", protoc);

    tonic_prost_build::configure()
        .build_client(true)
        .build_server(true)
        .file_descriptor_set_path(output.join("openengine_descriptor.bin"))
        .out_dir(&output)
        .compile_protos(&protos, &[proto_root, protobuf_include])?;

    Ok(())
}
