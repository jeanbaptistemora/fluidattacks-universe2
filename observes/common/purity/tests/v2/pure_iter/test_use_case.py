from purity.v2.pure_iter.factory import (
    from_range,
    infinite_range,
)
from tests.v2.pure_iter._utils import (
    assert_immutability,
    assert_immutability_inf,
)


def test_use_case_1() -> None:
    items = from_range(range(0, 10))
    mapped = items.map(lambda i: i + 2)
    assert mapped.to_list() == tuple(range(2, 12))
    r = items.map(lambda x: x * 2).chunked(3)
    expected = ((0, 2, 4), (6, 8, 10), (12, 14, 16), (18,))
    assert r.to_list() == expected
    assert_immutability(items)
    assert_immutability(mapped)


def test_inf() -> None:
    items = infinite_range(4, 10)
    for n, v in enumerate(items):
        assert v == 4 + (n * 10)
        if n > 15:
            break
    assert_immutability_inf(items)
