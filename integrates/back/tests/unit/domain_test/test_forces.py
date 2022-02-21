from dataloaders import (
    Dataloaders,
    get_new_context,
)
from forces.domain import (
    update_token,
)
from moto import (
    mock_secretsmanager,
)
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_update_secret_token() -> None:
    with mock_secretsmanager():
        loaders: Dataloaders = get_new_context()

        group_name = "unittesting"
        token = "mock token"
        assert await update_token(group_name, token)
        group = await loaders.group.load(group_name)
        assert group["agent_token"] == token

        group_name_no_token = "oneshottest"
        group_no_token = await loaders.group.load(group_name_no_token)
        assert group_no_token["agent_token"] is None
