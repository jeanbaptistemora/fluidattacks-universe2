# Standard library
from contextvars import (
    ContextVar,
    Token,
)
from contextlib import (
    asynccontextmanager,
)
from typing import (
    AsyncIterator,
)

# Third party libraries
import aiohttp
from aiogqlc import (
    GraphQLClient,
)

# State
API_TOKEN: ContextVar[str] = ContextVar('API_TOKEN', default='')


@asynccontextmanager
async def client() -> AsyncIterator[GraphQLClient]:
    if API_TOKEN.get():
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                verify_ssl=False,
            ),
            headers={
                'authorization': f'Bearer {API_TOKEN.get()}'
            },
            timeout=aiohttp.ClientTimeout(
                total=None,
                connect=None,
                sock_read=None,
                sock_connect=None,
            ),
            trust_env=True,
        ) as session:
            yield GraphQLClient(
                endpoint='https://fluidattacks.com/integrates/api',
                session=session
            )
    else:
        raise RuntimeError('create_session() must be called first')


def create_session(api_token: str) -> Token:
    return API_TOKEN.set(api_token)


def end_session(previous: Token) -> None:
    API_TOKEN.reset(previous)
