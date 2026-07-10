#!/usr/bin/env bash
set -euo pipefail

repository=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python=${PYTHON:-python3}
output="${repository}/packages/python/src"
export LC_ALL=C

if ! "${python}" -c "import grpc_tools.protoc" 2>/dev/null; then
  echo "grpcio-tools is required; install grpcio-tools==1.81.1" >&2
  exit 1
fi

protos=("${repository}"/proto/openengine/v1/*.proto)

for generated in \
  "${output}"/openengine/v1/*_pb2.py \
  "${output}"/openengine/v1/*_pb2.pyi \
  "${output}"/openengine/v1/*_pb2_grpc.py; do
  if [[ -e "${generated}" ]]; then
    rm -- "${generated}"
  fi
done

"${python}" -m grpc_tools.protoc \
  -I "${repository}/proto" \
  --python_out="${output}" \
  --pyi_out="${output}" \
  "${protos[@]}"

"${python}" -m grpc_tools.protoc \
  -I "${repository}/proto" \
  --grpc_python_out="${output}" \
  "${repository}/proto/openengine/v1/openengine.proto"
