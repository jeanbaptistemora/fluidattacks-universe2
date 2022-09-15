# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import aiohttp
from contextlib import (
    asynccontextmanager,
)
import requests
from typing import (
    Any,
    Dict,
    Optional,
)
from urllib3.exceptions import (
    InsecureRequestWarning,
)
from utils.function import (
    shield,
)
import warnings

RETRY = shield(
    on_error_return=None,
    retries=3,
    sleep_between_retries=3,
)


@asynccontextmanager  # type: ignore
async def create_session(  # type: ignore
    *args: Any,
    **kwargs: Any,
) -> aiohttp.ClientSession:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            # The server might be timing out the connection
            # since it's being used for multiple requests
            force_close=True,
            ssl=False,
        ),
        timeout=aiohttp.ClientTimeout(
            total=120,
            connect=None,
            sock_read=None,
            sock_connect=None,
        ),
        trust_env=True,
        *args,
        **kwargs,
    ) as session:
        yield session


@RETRY
async def request(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    *args: Any,
    **kwargs: Any,
) -> Optional[aiohttp.ClientResponse]:
    return await session.request(method, url, *args, **kwargs)


def request_blocking(
    url: str,
    headers: Dict[str, str],
) -> Optional[requests.Response]:
    try:
        warnings.simplefilter("ignore", InsecureRequestWarning)
        return requests.get(
            url,
            verify=False,  # nosec
            auth=None,
            headers=headers,
            stream=False,
            allow_redirects=True,
            timeout=10.0,
        )
    except requests.exceptions.RequestException:
        return None
    finally:
        warnings.simplefilter("default", InsecureRequestWarning)
