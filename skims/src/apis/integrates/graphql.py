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
from aiogqlc import GraphQLClient

# Context
SESSION: ContextVar[GraphQLClient] = ContextVar('SESSION')


@contextlib.asynccontextmanager
async def session(
    *,
    api_token: str,
    endpoint_url: str = 'https://fluidattacks.com/integrates/api',
) -> AsyncIterator[None]:
    client: GraphQLClient = GraphQLClient(
        endpoint=endpoint_url,
        headers={
            'authorization': f'Bearer {api_token}'
        },
    )

    token: Token[GraphQLClient] = SESSION.set(client)
    try:
        yield
    finally:
        SESSION.reset(token)
