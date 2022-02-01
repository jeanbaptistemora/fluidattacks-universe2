from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.pure_iter.factory import (
    from_range,
)
from purity.v2.stream.core import (
    Stream,
)
from purity.v2.stream.factory import (
    from_piter,
)
from secrets import (
    randbelow,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def _rand_int() -> Cmd[int]:
    return Cmd.from_cmd(lambda: randbelow(11))


def _assert_different_iter(stm: Stream[_T]) -> None:
    iter1 = unsafe_unwrap(stm._new_iter)
    iter2 = unsafe_unwrap(stm._new_iter)
    assert id(iter1) != id(iter2)


def test_map() -> None:
    items = from_range(range(10)).map(lambda _: _rand_int())
    stm = from_piter(items).map(lambda i: i + 1)
    _assert_different_iter(stm)


def test_chunked() -> None:
    items = from_range(range(10)).map(lambda _: _rand_int())
    stm = from_piter(items).chunked(2)
    _assert_different_iter(stm)
