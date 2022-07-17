try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
from ._schema_vesion import __schema_version__

__all__ = [
    "__version__",
    "__schema_version__",
]
