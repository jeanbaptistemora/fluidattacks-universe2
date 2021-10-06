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
from typing import (
    Callable,
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


class Test_PureIterFactory:
    @staticmethod
    def test_map_mutability() -> None:
        items_list = (1, 2, 3)
        piter = PureIterFactory.map(lambda x: x, items_list)
        assert_immutability(piter)

    @staticmethod
    def test_inf_map_mutability() -> None:
        piter = PureIterFactory.infinite_map(lambda x: x, 1, 1)
        assert_immutability_inf(piter)


class Test_PureIterIOFactory:
    @staticmethod
    def test_chain_mutability() -> None:
        items: PureIter[IO[Mappable[int]]] = PureIterFactory.map_range(
            mock_get, range(10)
        )
        chained = PureIterIOFactory.chain(items)
        assert_immutability(chained)
