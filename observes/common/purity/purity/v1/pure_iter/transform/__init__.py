from purity.v1._patch import (
    Patch,
)
from purity.v1.pure_iter._iter_factory import (
    IterableFactory,
)
from purity.v1.pure_iter._obj import (
    _PureIter,
    PureIter,
)
from returns.curry import (
    partial,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Callable,
    Optional,
    TypeVar,
)

_I = TypeVar("_I")
_R = TypeVar("_R")


def chain(
    unchained: PureIter[PureIter[_I]],
) -> PureIter[_I]:
    function = partial(IterableFactory.chain, unchained)
    return PureIter(_PureIter(Patch(function)))


def filter_opt(items: PureIter[Optional[_I]]) -> PureIter[_I]:
    draft = _PureIter(Patch(lambda: iter(IterableFactory.filter_none(items))))
    return PureIter(draft)


def until_none(items: PureIter[Optional[_I]]) -> PureIter[_I]:
    draft = _PureIter(Patch(lambda: iter(IterableFactory.until_none(items))))
    return PureIter(draft)


def until_empty(items: PureIter[Maybe[_I]]) -> PureIter[_I]:
    def _to_opt(item: Maybe[_I]) -> Optional[_I]:
        return item.value_or(None)

    opt: PureIter[Optional[_I]] = items.map(_to_opt)
    return until_none(opt)
