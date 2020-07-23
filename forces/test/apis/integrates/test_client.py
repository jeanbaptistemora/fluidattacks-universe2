# Third party libraries
import pytest

# Local libraries
from forces.apis.integrates.client import (
    get_transport,
    session,
)

# Third party libraries
from gql import (
    AIOHTTPTransport,
    gql
)


@pytest.mark.asyncio  # type: ignore
async def test_get_transport(
    test_token: str,
    test_endpoint: str,
) -> None:
    transport: AIOHTTPTransport = await get_transport(
        endpoint_url=test_endpoint, api_token=test_token)
    assert 'authorization' in transport.headers
    assert transport.headers['authorization'] == f'Bearer {test_token}'
    assert transport.url == test_endpoint
    await transport.connect()
    assert transport.session.closed == False
    await transport.close()
    assert transport.session is None


@pytest.mark.asyncio  # type: ignore
async def test_session(test_token: str, test_group: str) -> None:
    async with session(api_token=test_token) as client:
        query = gql("""
            query getGroup($name: String!){
                project(projectName: $name){
                    name
                }
            }
            """)
        result = await client.execute(
            query, variable_values={
                'name': test_group
            })
        assert result['project']['name'] == test_group
