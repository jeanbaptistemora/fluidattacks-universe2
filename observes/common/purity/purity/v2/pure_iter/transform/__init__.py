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
    IterableFactory,
)
from typing import (
    Optional,
    TypeVar,
)

_I = TypeVar("_I")


def chain(
    unchained: PureIter[PureIter[_I]],
) -> PureIter[_I]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactory.chain(unchained))
    )


def filter_opt(items: PureIter[Optional[_I]]) -> PureIter[_I]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactory.filter_none(items))
    )


def filter_maybe(items: PureIter[Maybe[_I]]) -> PureIter[_I]:
    return filter_opt(items.map(lambda x: x.value_or(None)))


def until_none(items: PureIter[Optional[_I]]) -> PureIter[_I]:
    return unsafe_from_generator(
        lambda: iter_obj(IterableFactory.until_none(items))
    )


def until_empty(items: PureIter[Maybe[_I]]) -> PureIter[_I]:
    def _to_opt(item: Maybe[_I]) -> Optional[_I]:
        return item.value_or(None)

    opt: PureIter[Optional[_I]] = items.map(_to_opt)
    return until_none(opt)
