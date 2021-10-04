from purity.v1 import (
    PureIterFactory,
)


def test_piter_mutability() -> None:
    items_list = (1, 2, 3)
    items = PureIterFactory.map(lambda x: x, items_list)
    for i, val in enumerate(items):
        assert items_list[i] == val
    for i, val in enumerate(items):
        assert items_list[i] == val
