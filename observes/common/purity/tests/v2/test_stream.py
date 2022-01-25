from black import (
    Optional,
    sys,
)
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.pure_iter.factory import (
    infinite_range,
)
from purity.v2.stream.factory import (
    from_piter,
)
from purity.v2.stream.transform import (
    until_none,
)
import pytest
from random import (
    randint,
)
from typing import (
    IO,
)


def _rand_val(count: int, none_index: int) -> Cmd[Optional[int]]:
    return Cmd.from_cmd(
        lambda: randint(0, 10) if count != none_index else None
    )


def test_use_case_1() -> None:
    with pytest.raises(SystemExit):
        none_index = 7
        data = (
            infinite_range(0, 1)
            .map(lambda x: _rand_val(x, none_index))
            .transform(lambda x: from_piter(x))
        )
        result = data.transform(lambda x: until_none(x)).map(lambda n: n * -1)

        def _verify(items: FrozenList[int]) -> None:
            assert len(items) == none_index
            for n in items:
                assert n <= 0

        verification = result.to_list().map(_verify)
        verification.compute()
