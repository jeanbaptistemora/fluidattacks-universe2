# Standard library
from typing import (
    Dict,
)

# Third party libraries
import aiohttp


async def get(method: str, url: str) -> Dict[str, str]:
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
    ) as session:
        response = await session.request(method, url)

        return response.headers
