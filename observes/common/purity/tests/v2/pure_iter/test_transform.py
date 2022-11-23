from purity.v2.cmd import (
    Cmd,
)
from purity.v2.pure_iter.factory import (
    from_flist,
    from_range,
)
from purity.v2.pure_iter.transform import (
    chain,
    consume,
    filter_opt,
    until_none,
)
import pytest
from tests.v2.pure_iter._utils import (
    assert_immutability,
)


def test_chain() -> None:
    base = (4, 78, 6)
    items = from_range(range(5)).map(lambda i: from_flist(base))
    chained = chain(items)
    assert_immutability(chained)
    assert tuple(chained) == base * 5


def test_consume() -> None:
    mutable_obj = [0]

    def _mutate(num: int) -> None:
        mutable_obj[0] = num

    items = from_flist(tuple(range(5))).map(
        lambda i: Cmd.from_cmd(lambda: _mutate(i))
    )
    assert_immutability(items, True)
    cmd = consume(items)
    assert mutable_obj[0] == 0

    def _verify(_: None) -> None:
        assert mutable_obj[0] == 4

    with pytest.raises(SystemExit):
        cmd.map(_verify).compute()


def test_filter_opt() -> None:
    items = tuple((0, 1, 2, 3, None, 4, 5, 6))
    result = filter_opt(from_flist(items))
    assert_immutability(result)
    assert tuple(result) == tuple(range(7))


def test_until_none() -> None:
    items = tuple((0, 1, 2, 3, None, 4, 5, 6))
    result = until_none(from_flist(items))
    assert_immutability(result)
    assert tuple(result) == tuple(range(4))
