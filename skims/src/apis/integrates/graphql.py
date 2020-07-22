# Standard library
import contextlib
from typing import (
    AsyncIterator,
)

# Third party libraries
from gql import (
    AIOHTTPTransport,
    Client,
)


def blocking_get_transport(
    *,
    api_token: str,
    endpoint_url: str,
) -> AIOHTTPTransport:
    return AIOHTTPTransport(
        headers={
            'authorization': f'Bearer {api_token}'
        },
        url=endpoint_url,
    )


@contextlib.asynccontextmanager
async def client(
    *,
    api_token: str,
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
) -> AsyncIterator[Client]:
    transport: AIOHTTPTransport = blocking_get_transport(
        api_token=api_token,
        endpoint_url=endpoint_url,
    )

    async with Client(
        execute_timeout=None,
        transport=transport,
    ) as session:
        yield session
