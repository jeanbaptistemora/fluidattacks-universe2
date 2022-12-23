from ._common import (
    get_group,
    get_token,
)
from code_etl.arm import (
    ArmClient,
    IgnoredPath,
)
from code_etl.parallel import (
    parallel_cmds,
)
from fa_purity import (
    FrozenList,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
import pytest
from typing import (
    FrozenSet,
)


def test_single() -> None:
    client = ArmClient.new(get_token())
    items = client.bind(lambda c: c.get_ignored_paths(get_group()))

    def _test(items: FrozenSet[IgnoredPath]) -> None:
        assert items

    with pytest.raises(SystemExit):
        items.map(_test).compute()


def test_stress() -> None:
    client = ArmClient.new(get_token())
    items = client.map(
        lambda c: tuple(c.get_ignored_paths(get_group()) for _ in range(100))
    ).bind(lambda x: parallel_cmds(x, 50))

    def _test(items: FrozenList[FrozenSet[IgnoredPath]]) -> None:
        assert items
        for i in items:
            assert i

    with pytest.raises(SystemExit):
        items.map(_test).compute()
