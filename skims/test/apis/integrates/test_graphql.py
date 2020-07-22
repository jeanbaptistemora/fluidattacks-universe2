# Local libraries
from apis.integrates.graphql import (
    client,
)

# Third party libraries
import pytest


@pytest.mark.asyncio  # type: ignore
async def test_client() -> None:
    async with client(
        api_token='fake',
        endpoint_url='fake',
    ) as graphql:
        assert graphql.client.transport.url == 'fake'
