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
    Union,
)


def test_piter_map_mutability() -> None:
    items_list = (1, 2, 3)
    items = PureIterFactory.map(lambda x: x, items_list)
    for i, val in enumerate(items):
        assert items_list[i] == val
    for i, val in enumerate(items):
        assert items_list[i] == val


def mock_get(_: int) -> IO[FrozenList[int]]:
    data = (randint(0, 10),)
    return IO(data)


def test_piter_chain_mutability() -> None:
    items: PureIter[IO[Mappable[int]]] = PureIterFactory.map_range(
        mock_get, range(10)
    )
    chained = PureIterIOFactory.chain(items)
    assert sum(1 for _ in chained) == sum(1 for _ in chained)


def test_piter_inf_map_mutability() -> None:
    items = PureIterFactory.infinite_map(lambda x: x, 1, 1)

    # assert sum(1 for _ in items) == sum(1 for _ in items)
    for i, val in enumerate(items, 1):
        assert i == val
        if i > 10:
            break
    for i, val in enumerate(items, 1):
        assert i == val
        if i > 10:
            break
