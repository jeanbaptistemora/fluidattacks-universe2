# Local libraries
from apis.integrates.graphql import (
    blocking_get_client,
)


def test_blocking_get_client() -> None:
    client = blocking_get_client(
        api_token='fake',
        endpoint_url='test'
    )

    assert client.endpoint == 'test'
