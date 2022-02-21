from forces.domain import (
    get_token,
    update_token,
)
from moto import (
    mock_secretsmanager,
)
import pytest

pytestmark = pytest.mark.asyncio


async def test_update_secret_token() -> None:
    with mock_secretsmanager():
        token = "mock token"
        result = await update_token("unittesting", token)
        assert result
        assert await get_token("unittesting") == token

        assert await get_token("unknown") is None
