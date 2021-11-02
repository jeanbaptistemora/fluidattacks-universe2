import functools
from purity.v1 import (
    FrozenList,
    PureIter,
)
from purity.v1.pure_iter import (
    factory,
    io_transform,
    transform,
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
    List,
    Optional,
    TypeVar,
)


def mock_get(_: int) -> IO[PureIter[int]]:
    data = (randint(0, 10), randint(0, 10))
    return IO(factory.from_flist(data))


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


class TestFactory:
    @staticmethod
    def test_from_flist() -> None:
        items = (1, 2, 3)
        piter = factory.from_flist(items)
        assert_immutability(piter)

    @staticmethod
    def test_from_range() -> None:
        piter = factory.from_range(range(10))
        assert_immutability(piter)

    @staticmethod
    def test_inf_range() -> None:
        piter = factory.infinite_range(1, 1)
        assert_immutability_inf(piter)


class TestSelfTransforms:
    @staticmethod
    def test_map() -> None:
        items = factory.from_flist((1, 2, 3))
        piter = items.map(lambda x: x)
        assert_immutability(piter)

    @staticmethod
    def test_chunked() -> None:
        items = factory.from_range(range(15))
        piter = items.chunked(5)
        assert_immutability(piter)
        assert sum(1 for _ in piter) == 3
        for sub_piter in piter:
            assert_immutability(sub_piter)
            assert sum(1 for _ in sub_piter) == 5
        module: List[int] = []
        assert functools.reduce(
            lambda a, b: list(a) + list(b), piter, module
        ) == list(items)


class TestTransforms:
    @staticmethod
    def test_chain() -> None:
        items = factory.from_flist(
            (
                factory.from_flist((1, 2, 3)),
                factory.from_flist((1, 2, 3)),
            )
        )
        piter = transform.chain(items)
        assert_immutability(piter)

    @staticmethod
    def test_filter_opt() -> None:
        data = (1, None, 2, None, 3, None)
        items = factory.from_flist(data)
        piter = transform.filter_opt(items)
        assert_immutability(piter)
        assert sum(1 for _ in piter) == 3

    @staticmethod
    def test_until_none() -> None:
        raw: FrozenList[Optional[int]] = (1, 2, None, 5, 6)
        items = factory.from_flist(raw)
        filtered = transform.until_none(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (1, 2)

    @staticmethod
    def test_until_empty() -> None:
        raw = factory.from_flist((1, 2, None, 5, 6))
        items = raw.map(lambda x: Maybe.from_optional(x))
        filtered = transform.until_empty(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (1, 2)


class TestiIoTransforms:
    @staticmethod
    def test_chain() -> None:
        items: PureIter[IO[PureIter[int]]] = factory.from_range(range(10)).map(
            mock_get
        )
        chained = io_transform.chain(items)
        assert_immutability(chained)

    @staticmethod
    def test_until_none() -> None:
        raw = factory.from_flist((1, 2, None, 5, 6))
        items = raw.map(lambda x: IO(x))
        filtered = io_transform.until_none(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (IO(1), IO(2))

    @staticmethod
    def test_until_empty() -> None:
        raw = factory.from_flist((1, 2, None, 5, 6))
        items = raw.map(lambda x: IO(Maybe.from_optional(x)))
        filtered = io_transform.until_empty(items)
        assert_immutability(filtered)
        assert tuple(filtered) == (IO(1), IO(2))
