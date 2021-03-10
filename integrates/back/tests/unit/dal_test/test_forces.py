import pytest
from botocore.exceptions import ClientError
from moto import mock_secretsmanager

from forces.dal import (
    create_execution,
    get_secret_token,
    update_secret_token,
)
from newutils import datetime as datetime_utils


pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution():
    group = "unittesting"
    execution_id = "random_id"
    now = datetime_utils.get_now()
    assert await create_execution(
        project_name=group,
        execution_id=execution_id,
        date=now,
    )


async def test_update_secret_token() -> None:
    with mock_secretsmanager():
        token = 'mock token'
        result = await update_secret_token('unittesting', token)
        assert result
        assert await get_secret_token('unittesting') == token

        assert await get_secret_token('unknown') is None
