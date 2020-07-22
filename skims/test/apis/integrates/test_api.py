# Third party libraries
import pytest

# Local libraries
from apis.integrates.api import (
    get_group_level_role,
)
from apis.integrates.graphql import (
    session,
    SESSION,
)


@pytest.mark.asyncio  # type: ignore
async def test_get_group_level_role(
    test_group: str,
    test_token: str,
) -> None:
    async with session(api_token=test_token):
        assert await get_group_level_role(group=test_group) == 'admin'
