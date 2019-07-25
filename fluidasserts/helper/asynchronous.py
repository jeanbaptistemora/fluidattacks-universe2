# -*- coding: utf-8 -*-

"""This module provide support for Asynchronous python."""

# standard imports
import asyncio
from typing import Any, List, Callable

# 3rd party imports
import aiohttp

# local imports


def is_timeout_error(obj: Any) -> bool:
    """Return True if obj is an instance of a timeout error."""
    timeout_errors = (
        asyncio.TimeoutError,
        aiohttp.client_exceptions.ServerTimeoutError,
    )
    return isinstance(obj, timeout_errors)


def is_connection_error(obj: Any) -> bool:
    """Return True if obj is an instance of a connection error."""
    connection_errors = (
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
    return isinstance(obj, connection_errors)


def is_parameter_error(obj: Any) -> bool:
    """Return True if obj is an instance of a parameter error."""
    parameter_errors = (
        aiohttp.http.WebSocketError,
        aiohttp.client_exceptions.InvalidURL,
    )
    return isinstance(obj, parameter_errors)


def run_func(func: Callable,
             args: list,
             return_exceptions: bool = True) -> List[Any]:
    """Run a function asynchronously over the list of arguments."""
    loop = asyncio.new_event_loop()
    future = asyncio.gather(*(func(*a, **k) for a, k in args),
                            return_exceptions=return_exceptions,
                            loop=loop)
    result = loop.run_until_complete(future)
    loop.close()
    return result
