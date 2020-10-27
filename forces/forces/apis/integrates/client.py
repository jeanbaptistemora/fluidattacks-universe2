"""Fluid Forces Integrates api client."""
# Standard library
import contextlib
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
import aiohttp
from aiogqlc import GraphQLClient

# Local libraries
from forces.apis.integrates import (
    get_api_token,
)

# Context
SESSION: ContextVar[GraphQLClient] = ContextVar('SESSION')
TVar = TypeVar('TVar')


@contextlib.asynccontextmanager
async def session(
    api_token: str = '',
    endpoint_url: str = 'https://integrates.fluidattacks.com/api',
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
                  operation_name: str,
                  variables: Optional[Dict[str, Any]] = None,
                  default: Optional[Any] = None,
                  **kwargs: Any) -> TVar:
    async with session(**kwargs) as client:
        result: Any = dict()
        response: aiohttp.ClientResponse

        response = await client.execute(
            query,
            variables=variables,
            operation=operation_name,
        )
        result = await response.json()

        if 'errors' in result.keys():
            raise Exception(*result['errors'])

        result = result.get('data', dict())
        return result or default  # type: ignore
