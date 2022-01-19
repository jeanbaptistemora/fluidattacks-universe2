from collections import (
    deque,
)
from purity.v2.maybe import (
    Maybe,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.pure_iter.factory import (
    iter_obj,
    unsafe_from_generator,
)
from purity.v2.pure_iter.transform._iter_factory import (
    IterableFactoryIO,
)
from returns.io import (
    IO,
)
from typing import (
    Optional,
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


def until_none(items: PureIter[IO[Optional[_I]]]) -> PureIter[IO[_I]]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactoryIO.filter_io(items))
    )


def until_empty(items: PureIter[IO[Maybe[_I]]]) -> PureIter[IO[_I]]:
    def _to_opt(item: IO[Maybe[_I]]) -> IO[Optional[_I]]:
        return item.map(lambda i: i.value_or(None))

    opt: PureIter[IO[Optional[_I]]] = items.map(_to_opt)
    return until_none(opt)
