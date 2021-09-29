from paginator.v2 import (
    AllPages,
    PageGetter,
    PageGetterIO,
    PageId,
    PageOrAll,
    PageResult,
)
from typing import (
    NamedTuple,
)
import warnings

warnings.warn("use paginator.v2 instead", DeprecationWarning, stacklevel=2)


class Limits(NamedTuple):
    max_calls: int
    max_period: float
    min_period: float
    greediness: int


DEFAULT_LIMITS = Limits(
    max_calls=5,
    max_period=1,
    min_period=0.2,
    greediness=10,
)


__all__ = [
    "AllPages",
    "PageId",
    "PageOrAll",
    "PageResult",
    "PageGetter",
    "PageGetterIO",
]
