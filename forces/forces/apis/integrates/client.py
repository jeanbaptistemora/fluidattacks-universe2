"""Fluid Forces Integrates api client."""
# Standard library
import contextlib
from contextvars import (
    ContextVar,
    Token,
)
from typing import (
    Any,
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
from forces.utils.aio import (
    unblock,
)

from forces.apis.integrates import (
    get_api_token,
)

# Context
SESSION: ContextVar[AsyncClientSession] = ContextVar('SESSION')


async def get_transport(
        *,
        api_token: str,
        endpoint_url: str,
        **kwargs: Any
) -> AIOHTTPTransport:
    """Returns an AIOHTTPTransport."""

    def _get_transport() -> AIOHTTPTransport:
        return AIOHTTPTransport(
            headers={'authorization': f'Bearer {api_token}'},
            url=endpoint_url,
            **kwargs
        )

    return await unblock(_get_transport)


@contextlib.asynccontextmanager
async def session(
        api_token: str = get_api_token(),
        endpoint_url: str = 'https://fluidattacks.com/integrates/api',
        **kwargs: str,
) -> AsyncIterator[Client]:
    """Returns an Async GraphQL Client."""
    transport: AIOHTTPTransport = await get_transport(
        api_token=api_token,
        endpoint_url=endpoint_url,
        **kwargs
    )
    async with Client(
            execute_timeout=None,
            transport=transport,
    ) as client_session:
        token: Token[Any] = SESSION.set(client_session)
        try:
            yield SESSION.get()
        finally:
            SESSION.reset(token)
