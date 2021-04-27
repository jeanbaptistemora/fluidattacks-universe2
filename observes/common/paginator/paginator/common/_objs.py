# Standard libraries
from typing import (
    NamedTuple,
)


class AllPages(NamedTuple):
    pass


class EmptyPage(NamedTuple):
    pass


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
