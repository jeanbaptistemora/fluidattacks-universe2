from ._common import (
    get_group,
    get_token,
)
from code_etl.arm import (
    ArmClient,
)
from code_etl.parallel import (
    parallel_cmds,
)
import pytest


def test_single() -> None:
    client = ArmClient.new(get_token())
    items = client.bind(lambda c: c.get_org(get_group()))

    with pytest.raises(SystemExit):
        items.map(lambda x: x.unwrap()).compute()


def test_stress() -> None:
    client = ArmClient.new(get_token())
    items = client.map(
        lambda c: tuple(c.get_org(get_group()) for _ in range(100))
    ).bind(lambda x: parallel_cmds(x, 50))

    with pytest.raises(SystemExit):
        items.map(lambda rs: (r.unwrap() for r in rs)).compute()
