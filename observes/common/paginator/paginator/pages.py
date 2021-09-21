from paginator.v2 import (
    AllPages,
    DEFAULT_LIMITS,
    Limits,
    PageGetter,
    PageGetterIO,
    PageId,
    PageOrAll,
    PageResult,
)
import warnings

warnings.warn("use paginator.v2 instead", DeprecationWarning, stacklevel=2)

__all__ = [
    "AllPages",
    "PageId",
    "PageOrAll",
    "Limits",
    "DEFAULT_LIMITS",
    "PageResult",
    "PageGetter",
    "PageGetterIO",
]
