from collections import (
    deque,
)
from purity.v1.pure_iter.core import (
    PureIter,
)
from purity.v1.pure_iter.factory import (
    iter_obj,
    unsafe_from_generator,
)
from purity.v1.pure_iter.transform._iter_factory import (
    IterableFactoryIO,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    TypeVar,
)

_I = TypeVar("_I")


def chain(
    unchained: PureIter[IO[PureIter[_I]]],
) -> PureIter[IO[_I]]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactoryIO.chain_io(unchained))
    )


def consume(p_iter: PureIter[IO[None]]) -> IO[None]:
    deque(p_iter, maxlen=0)
    return IO(None)


def until_none(items: PureIter[IO[_I | None]]) -> PureIter[IO[_I]]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactoryIO.filter_io(items))
    )


def until_empty(items: PureIter[IO[Maybe[_I]]]) -> PureIter[IO[_I]]:
    def _to_opt(item: IO[Maybe[_I]]) -> IO[_I | None]:
        return item.map(lambda i: i.value_or(None))

    opt: PureIter[IO[_I | None]] = items.map(_to_opt)
    return until_none(opt)
