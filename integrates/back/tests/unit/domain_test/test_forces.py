from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
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
        await update_token(group_name, token)
        group: Group = await loaders.group_typed.load(group_name)
        assert group.agent_token == token

        await update_token(group_name, None)
        loaders.group_typed.clear(group_name)
        group = await loaders.group_typed.load(group_name)
        assert group.agent_token is None

        group_name_no_token = "oneshottest"
        group_no_token: Group = await loaders.group_typed.load(
            group_name_no_token
        )
        assert group_no_token.agent_token is None
