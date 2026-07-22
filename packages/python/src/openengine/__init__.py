"""Generated Python bindings for the OpenEngine protocol."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("openengine-proto")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

SCHEMA_REVISION = 3
MINIMUM_CLIENT_REVISION = 1
# Package versions do not identify a path/Git dependency's exact source. Engine
# servers must replace this sentinel with the immutable commit SHA or signed tag
# they were built against.
SCHEMA_RELEASE = "unreleased"

__all__ = [
    "MINIMUM_CLIENT_REVISION",
    "SCHEMA_RELEASE",
    "SCHEMA_REVISION",
    "__version__",
]
