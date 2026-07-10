"""Generated Python bindings for the OpenEngine protocol."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("openengine-proto")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

SCHEMA_REVISION = 1
SCHEMA_RELEASE = (
    "unreleased" if __version__ == "0.0.0+local" else f"v{__version__}"
)

__all__ = ["SCHEMA_RELEASE", "SCHEMA_REVISION", "__version__"]
