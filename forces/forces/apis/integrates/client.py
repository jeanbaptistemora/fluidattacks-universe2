"""Fluid Forces Integrates api client."""
# Standard library
import contextlib
import sys
from contextvars import (
    ContextVar,
    Token,
)
from typing import (
    Any,
    Dict,
    AsyncIterator,
    TypeVar,
    Optional,
)

# Third party libraries
import bugsnag
from aiohttp.client_exceptions import (
    ClientConnectorError,
)
from gql.client import (
    AsyncClientSession,
)
from gql import (
    AIOHTTPTransport,
    Client,
    gql,
)
from gql.transport.exceptions import (
    TransportQueryError,
)

# Local libraries
from forces.apis.integrates import (
    get_api_token,
)
from forces.utils.logs import (
    log,
)
from forces.utils.aio import (
    unblock,)
# Context
SESSION: ContextVar[AsyncClientSession] = ContextVar('SESSION')
TVar = TypeVar('TVar')


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


async def execute(query: str,
                  variables: Optional[Dict[str, Any]] = None,
                  default: Optional[Any] = None,
                  **kwargs: Any) -> TVar:
    async with session(**kwargs) as client:
        gql_query = gql(query)
        response: Any = default
        exc_metadata: Dict[str, Any] = {
            'parameters': {
                'query': query,
                'default': default,
                'variables': variables,
                **kwargs
            }
        }
        try:
            response = await client.execute(gql_query,
                                            variable_values=variables)
        except ClientConnectorError as exc:
            await log('error', str(exc))
            await unblock(bugsnag.notify,
                          exc,
                          metadata=exc_metadata,
                          context='integrates_api')
            sys.exit(1)
        except TransportQueryError as exc:
            await log('warning', ('The token may be invalid or does '
                                  'not have the required permissions'))
            await log('error', exc.errors[0]['message'])
            await unblock(bugsnag.notify,
                          exc,
                          metadata=exc_metadata,
                          context='integrates_api')
        return response  # type: ignore
