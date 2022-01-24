from collections import (
    deque,
)
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from typing import (
    Iterable,
    TypeVar,
)

_T = TypeVar("_T")


def _deque(items: Iterable[_T]) -> None:
    deque(items, maxlen=0)


def consume(p_iter: PureIter[Cmd[None]]) -> Cmd[None]:
    return Cmd.from_cmd(lambda: _deque(iter(unsafe_unwrap(a) for a in p_iter)))
