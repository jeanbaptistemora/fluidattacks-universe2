from purity.v1 import (
    FrozenList,
    Mappable,
    PureIter,
    PureIterFactory,
    PureIterIOFactory,
)
from random import (
    randint,
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


def mock_get(_: int) -> IO[FrozenList[int]]:
    data = (randint(0, 10), randint(0, 10))
    return IO(data)


_T = TypeVar("_T")


def count(piter: PureIter[_T], limit: int) -> int:
    n_items = 0
    for _ in piter:
        n_items += 1
        if n_items >= limit:
            break
    return n_items


def assert_immutability(piter: PureIter[_T]) -> None:
    # for finite PureIter
    assert sum(1 for _ in piter) == sum(1 for _ in piter)


def assert_immutability_inf(piter: PureIter[_T]) -> None:
    # for infinite PureIter
    assert count(piter, 10) == count(piter, 10)


class TestPureIterFactory:
    @staticmethod
    def test_chain() -> None:
        data = ((1, 2, 3), (1, 2, 3))
        items: PureIter[Mappable[int]] = PureIterFactory.from_flist(data)
        piter = PureIterFactory.chain(items)
        assert_immutability(piter)

    @staticmethod
    def test_from_flist() -> None:
        items = (1, 2, 3)
        piter = PureIterFactory.from_flist(items)
        assert_immutability(piter)

    @staticmethod
    def test_filter() -> None:
        data = (1, None, 2, None, 3, None)
        items = PureIterFactory.from_flist(data)
        piter = PureIterFactory.filter(items)
        assert_immutability(piter)
        assert sum(1 for _ in piter) == 3

    @staticmethod
    def test_map() -> None:
        items = (1, 2, 3)
        piter = PureIterFactory.map(lambda x: x, items)
        assert_immutability(piter)

    @staticmethod
    def test_map_range() -> None:
        items = range(10)
        piter = PureIterFactory.map_range(lambda x: x, items)
        assert_immutability(piter)

    @staticmethod
    def test_inf_map() -> None:
        piter = PureIterFactory.infinite_map(lambda x: x, 1, 1)
        assert_immutability_inf(piter)

    @staticmethod
    def test_until_none() -> None:
        raw: FrozenList[Optional[int]] = (1, 2, None, 5, 6)
        items = PureIterFactory.from_flist(raw)
        filtered = PureIterFactory.until_none(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (1, 2)

    @staticmethod
    def test_until_empty() -> None:
        raw: FrozenList[Optional[int]] = (1, 2, None, 5, 6)
        items = PureIterFactory.map(lambda x: Maybe.from_optional(x), raw)
        filtered = PureIterFactory.until_empty(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (1, 2)


class TestPureIterIOFactory:
    @staticmethod
    def test_chain() -> None:
        items: PureIter[IO[Mappable[int]]] = PureIterFactory.map_range(
            mock_get, range(10)
        )
        chained = PureIterIOFactory.chain(items)
        assert_immutability(chained)

    @staticmethod
    def test_until_none() -> None:
        raw: FrozenList[Optional[int]] = (1, 2, None, 5, 6)
        items = PureIterFactory.map(lambda x: IO(x), raw)
        filtered = PureIterIOFactory.until_none(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (IO(1), IO(2))

    @staticmethod
    def test_until_empty() -> None:
        raw: FrozenList[Optional[int]] = (1, 2, None, 5, 6)
        items = PureIterFactory.map(lambda x: IO(Maybe.from_optional(x)), raw)
        filtered = PureIterIOFactory.until_empty(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (IO(1), IO(2))
