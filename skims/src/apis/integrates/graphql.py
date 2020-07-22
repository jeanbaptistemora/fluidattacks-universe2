# Standard library
import contextlib
from contextvars import (
    ContextVar,
    Token,
)
from typing import (
    AsyncIterator,
)

# Third party libraries
from gql import (
    AIOHTTPTransport,
    Client,
)
from gql.client import (
    AsyncClientSession,
)

# Local libraries
from utils.aio import (
    unblock,
)

# Context
SESSION: ContextVar[AsyncClientSession] = ContextVar('SESSION')


async def get_transport(
    *,
    api_token: str,
    endpoint_url: str,
) -> AIOHTTPTransport:

    def _get_transport():
        return AIOHTTPTransport(
            headers={
                'authorization': f'Bearer {api_token}'
            },
            url=endpoint_url,
        )

    return await unblock(_get_transport)


@contextlib.asynccontextmanager
async def session(
    *,
    api_token: str,
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
) -> AsyncIterator[None]:
    transport: AIOHTTPTransport = await get_transport(
        api_token=api_token,
        endpoint_url=endpoint_url,
    )

    async with Client(
        execute_timeout=None,
        transport=transport,
    ) as client_session:
        token: Token = SESSION.set(client_session)
        try:
            yield
        finally:
            SESSION.reset(token)
