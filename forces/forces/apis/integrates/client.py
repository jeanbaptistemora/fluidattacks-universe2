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
    ClientResponseError,
    ServerDisconnectedError
)
import aiohttp
from aiogqlc import GraphQLClient

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
SESSION: ContextVar[GraphQLClient] = ContextVar('SESSION')
TVar = TypeVar('TVar')


@contextlib.asynccontextmanager
async def session(
    api_token: str = '',
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
    **kwargs: str,
) -> AsyncIterator[GraphQLClient]:
    """Returns an Async GraphQL Client."""
    try:
        yield SESSION.get()
    except LookupError:
        api_token = api_token or get_api_token()
        async with aiohttp.ClientSession(headers={
                'authorization': f'Bearer {api_token}',
                'Connection': "close",
                **kwargs
        }, ) as client_session:
            client = GraphQLClient(endpoint_url, session=client_session)
            token: Token[Any] = SESSION.set(client)
            try:
                yield SESSION.get()
            finally:
                SESSION.reset(token)


async def execute(query: str,
                  variables: Optional[Dict[str, Any]] = None,
                  default: Optional[Any] = None,
                  **kwargs: Any) -> TVar:
    async with session(**kwargs) as client:
        result: Any = dict()
        response: aiohttp.ClientResponse
        exc_metadata: Dict[str, Any] = {
            'parameters': {
                'query': query,
                'default': default,
                'variables': variables,
                **kwargs
            }
        }
        try:
            response = await client.execute(query, variables=variables)
            result = await response.json()
        except (ClientConnectorError, ServerDisconnectedError) as exc:
            await log('error', str(exc))
            await unblock(bugsnag.notify,
                          exc,
                          metadata=exc_metadata,
                          context='integrates_api')
            sys.exit(1)
        except ClientResponseError as exc:
            await log('error', exc.message)
            await unblock(bugsnag.notify,
                          exc,
                          metadata=exc_metadata,
                          context='integrates_api')

        if 'errors' in result.keys():
            for error in result['errors']:
                await log('error', error['message'])

        result = result.get('data', dict())
        return result or default  # type: ignore
