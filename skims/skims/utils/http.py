# Local libraries
from contextlib import (
    asynccontextmanager,
)
from typing import (
    Any,
)

# Third party libraries
import aiohttp

# Local libraries
from utils.function import (
    shield,
)


RETRY = shield(retries=3, sleep_between_retries=1)


@asynccontextmanager
async def create_session(*args: Any, **kwargs: Any) -> aiohttp.ClientSession:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=False,
        ),
        timeout=aiohttp.ClientTimeout(
            total=60,
            connect=None,
            sock_read=None,
            sock_connect=None,
        ),
        trust_env=True,
        *args, **kwargs,
    ) as session:
        yield session


@RETRY
async def request(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
) -> aiohttp.ClientResponse:
    return await session.request(method, url)
