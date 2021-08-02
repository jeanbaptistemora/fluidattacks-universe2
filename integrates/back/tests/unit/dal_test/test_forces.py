from forces.dal import (
    add_execution,
    get_secret_token,
    update_secret_token,
)
from moto import (
    mock_secretsmanager,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution() -> None:
    group = "unittesting"
    execution_id = "random_id"
    now = datetime_utils.get_now()
    assert await add_execution(
        group_name=group,
        execution_id=execution_id,
        date=now,
    )


async def test_update_secret_token() -> None:
    with mock_secretsmanager():
        token = "mock token"
        result = await update_secret_token("unittesting", token)
        assert result
        assert await get_secret_token("unittesting") == token

        assert await get_secret_token("unknown") is None
