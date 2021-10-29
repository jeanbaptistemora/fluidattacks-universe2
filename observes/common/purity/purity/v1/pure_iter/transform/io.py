from purity.v1._patch import (
    Patch,
)
from purity.v1.pure_iter._iter_factory import (
    IterableFactoryIO,
)
from purity.v1.pure_iter._obj import (
    _PureIter,
    PureIter,
)
from returns.curry import (
    partial,
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
_R = TypeVar("_R")


def chain(
    unchained: PureIter[IO[PureIter[_I]]],
) -> PureIter[IO[_I]]:
    function = partial(IterableFactoryIO.chain_io, unchained)
    return PureIter(_PureIter(Patch(function)))


def until_none(items: PureIter[IO[Optional[_I]]]) -> PureIter[IO[_I]]:
    draft = _PureIter(Patch(lambda: iter(IterableFactoryIO.filter_io(items))))
    return PureIter(draft)


def until_empty(items: PureIter[IO[Maybe[_I]]]) -> PureIter[IO[_I]]:
    def _to_opt(item: IO[Maybe[_I]]) -> IO[Optional[_I]]:
        return item.map(lambda i: i.value_or(None))

    opt: PureIter[IO[Optional[_I]]] = items.map(_to_opt)
    return until_none(opt)
