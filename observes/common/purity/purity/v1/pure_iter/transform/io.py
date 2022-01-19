from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.pure_iter.transform.io import (
    chain,
    consume,
    until_none,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Optional,
    TypeVar,
)

_I = TypeVar("_I")


def until_empty(items: PureIter[IO[Maybe[_I]]]) -> PureIter[IO[_I]]:
    def _to_opt(item: IO[Maybe[_I]]) -> IO[Optional[_I]]:
        return item.map(lambda i: i.value_or(None))

    opt: PureIter[IO[Optional[_I]]] = items.map(_to_opt)
    return until_none(opt)


__all__ = [
    "chain",
    "consume",
    "until_none",
]
