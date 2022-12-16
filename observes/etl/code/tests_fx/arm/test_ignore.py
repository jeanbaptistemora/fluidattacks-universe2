from ._common import (
    get_group,
    get_token,
)
from code_etl.arm import (
    ArmClient,
    IgnoredPath,
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
