# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""This module provide support for Asynchronous python."""


import aiohttp
import asyncio
import functools
import time
from typing import (
    Any,
    Callable,
    List,
)

# Constants
TIMEOUT_ERRORS = (
    asyncio.TimeoutError,
    aiohttp.client_exceptions.ServerTimeoutError,
)
PARAMETER_ERRORS = (
    aiohttp.http.WebSocketError,
    aiohttp.client_exceptions.InvalidURL,
)
CONNECTION_ERRORS = (
    aiohttp.client_exceptions.ClientConnectionError,
    aiohttp.client_exceptions.ClientConnectorCertificateError,
    aiohttp.client_exceptions.ClientConnectorError,
    aiohttp.client_exceptions.ClientConnectorSSLError,
    aiohttp.client_exceptions.ClientError,
    aiohttp.client_exceptions.ClientHttpProxyError,
    aiohttp.client_exceptions.ClientOSError,
    aiohttp.client_exceptions.ClientPayloadError,
    aiohttp.client_exceptions.ClientProxyConnectionError,
    aiohttp.client_exceptions.ClientResponseError,
    aiohttp.client_exceptions.ClientSSLError,
    aiohttp.client_exceptions.ContentTypeError,
    aiohttp.client_exceptions.ServerConnectionError,
    aiohttp.client_exceptions.ServerDisconnectedError,
    aiohttp.client_exceptions.WSServerHandshakeError,
)


def is_timeout_error(obj: Any) -> bool:
    """Return True if obj is an instance of a timeout error."""
    return isinstance(obj, TIMEOUT_ERRORS)


def is_connection_error(obj: Any) -> bool:
    """Return True if obj is an instance of a connection error."""
    return isinstance(obj, CONNECTION_ERRORS)


def is_parameter_error(obj: Any) -> bool:
    """Return True if obj is an instance of a parameter error."""
    return isinstance(obj, PARAMETER_ERRORS)


def run_func(
    func: Callable, args: list, return_exceptions: bool = True
) -> List[Any]:
    """Run a function asynchronously over the list of arguments."""
    loop = asyncio.new_event_loop()
    results: list = []
    # Warning before raising this number up:
    #   too many DNS lookups made asynchronously break the OS with
    #   impossible-to-catch errors, the logic below buffers the number of
    #   futures that are collected to a number that is reasonably low
    #   compared to the maximum number of file descriptors provided by the OS
    results_per_loop: int = 64
    for index in range(0, len(args), results_per_loop):
        future = asyncio.gather(
            *(
                asyncio.ensure_future(func(*a, **k), loop=loop)
                for a, k in args[index : index + results_per_loop]
            ),
            return_exceptions=return_exceptions,
            loop=loop,
        )
        result = loop.run_until_complete(future)
        results.extend(result)
    loop.close()
    return results


def http_retry(func: Callable) -> Callable:
    """Decorator to retry the function if a connection error is raised."""

    @functools.wraps(func)
    async def decorated(*args, **kwargs) -> Any:  # noqa
        """Retry the function if a ConnError is raised."""
        if kwargs.get("retry"):
            for _ in range(5):
                try:
                    return await func(*args, **kwargs)
                except CONNECTION_ERRORS:
                    # Wait some seconds and retry
                    await time.sleep(1.0)
        return await func(*args, **kwargs)

    return decorated
