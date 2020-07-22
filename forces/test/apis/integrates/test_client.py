# Third party libraries
import pytest

# Local libraries
from forces.apis.integrates import client

# Third party libraries
from gql import (
    AIOHTTPTransport,
)


@pytest.mark.asyncio  # type: ignore
async def test_get_transport(
    test_token: str,
    test_endpoint: str,
) -> None:
    transport: AIOHTTPTransport = await client.get_transport(
        endpoint_url=test_endpoint, api_token=test_token)
    assert 'authorization' in transport.headers
    assert transport.headers['authorization'] == f'Bearer {test_token}'
    assert transport.url == test_endpoint
    await transport.connect()
    assert transport.session.closed == False
    await transport.close()
    assert transport.session is None
