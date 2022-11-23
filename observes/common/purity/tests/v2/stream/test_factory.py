from purity.v2.pure_iter.factory import (
    from_range,
)
from purity.v2.stream.factory import (
    from_piter,
)
from tests.v2.stream._utils import (
    assert_different_iter,
    rand_int,
)


def test_from_piter() -> None:
    items = from_range(range(10)).map(lambda _: rand_int())
    stm = from_piter(items)
    assert_different_iter(stm)
