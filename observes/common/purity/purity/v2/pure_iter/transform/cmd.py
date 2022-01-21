from collections import (
    deque,
)
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.maybe import (
    Maybe,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.pure_iter.factory import (
    unsafe_from_cmd,
)
from purity.v2.pure_iter.transform._iter_factory import (
    IterableFactoryCmd,
)
from typing import (
    Iterable,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


def chain(
    unchained: PureIter[Cmd[PureIter[_T]]],
) -> PureIter[Cmd[_T]]:
    return unsafe_from_cmd(
        Cmd.from_cmd(lambda: IterableFactoryCmd.chain_io(unchained))
    )


def _deque(items: Iterable[_T]) -> None:
    deque(items, maxlen=0)


def consume(p_iter: PureIter[Cmd[None]]) -> Cmd[None]:
    return Cmd.from_cmd(lambda: _deque(iter(unsafe_unwrap(a) for a in p_iter)))


def until_none(items: PureIter[Cmd[Optional[_T]]]) -> PureIter[Cmd[_T]]:
    return unsafe_from_cmd(
        Cmd.from_cmd(lambda: IterableFactoryCmd.until_none(items))
    )


def until_empty(items: PureIter[Cmd[Maybe[_T]]]) -> PureIter[Cmd[_T]]:
    _items = items.map(lambda c: c.map(lambda m: m.value_or(None)))
    return until_none(_items)
