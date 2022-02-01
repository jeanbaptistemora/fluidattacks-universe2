from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.stream.core import (
    Stream,
)
from secrets import (
    randbelow,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def rand_int() -> Cmd[int]:
    return Cmd.from_cmd(lambda: randbelow(11))


def assert_different_iter(stm: Stream[_T]) -> None:
    iter1 = unsafe_unwrap(stm._new_iter)
    iter2 = unsafe_unwrap(stm._new_iter)
    assert id(iter1) != id(iter2)
