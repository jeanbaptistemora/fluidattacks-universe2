# Local libraries
from apis.integrates.graphql import (
    session,
    SESSION,
)

# Third party libraries
import pytest


@pytest.mark.asyncio  # type: ignore
async def test_session() -> None:
    async with session(
        api_token='fake',
        endpoint_url='fake',
    ):
        assert SESSION.get().transport.url == 'fake'
