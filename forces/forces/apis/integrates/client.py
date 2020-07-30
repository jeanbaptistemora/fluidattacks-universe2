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
from forces.apis.integrates import (
    get_api_token,
)

# Context
SESSION: ContextVar[AsyncClientSession] = ContextVar('SESSION')


def get_transport(
        *,
        api_token: str,
        endpoint_url: str,
        **kwargs: Any
) -> AIOHTTPTransport:
    """Returns an AIOHTTPTransport."""
    return AIOHTTPTransport(
        headers={'authorization': f'Bearer {api_token}'},
        url=endpoint_url,
        **kwargs)


@contextlib.asynccontextmanager
async def session(
        api_token: str = '',
        endpoint_url: str = 'https://fluidattacks.com/integrates/api',
        **kwargs: str,
) -> AsyncIterator[Client]:
    """Returns an Async GraphQL Client."""
    try:
        yield SESSION.get()
    except LookupError:
        api_token = api_token or get_api_token()
        transport: AIOHTTPTransport = get_transport(
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
