from purity.v2.cmd import (
    Cmd,
)
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.pure_iter.factory import (
    from_flist,
    from_range,
)
from purity.v2.stream.factory import (
    from_piter,
)
from purity.v2.stream.transform import (
    chain,
    squash,
)
import pytest
from tests.v2.stream._utils import (
    assert_different_iter,
    rand_int,
)


def test_chain() -> None:
    base = (1, 2, 3)
    items = from_flist(base).map(lambda i: Cmd.from_cmd(lambda: i))
    stm = from_piter(items)
    unchained = from_piter(
        from_range(range(10)).map(
            lambda _: stm.to_list().map(lambda x: from_flist(x))
        )
    )
    chained = chain(unchained)
    assert_different_iter(chained)

    def _verify(elements: FrozenList[int]) -> None:
        assert elements == base * 10

    with pytest.raises(SystemExit):
        chained.to_list().map(_verify).compute()


def test_squash() -> None:
    items = from_range(range(10)).map(lambda _: rand_int())
    stm = from_piter(items).map(lambda _: rand_int())
    result = squash(stm)
    assert_different_iter(result)
