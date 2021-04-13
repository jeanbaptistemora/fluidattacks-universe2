# Starlette middlewares file

# Standard library
from collections import defaultdict
from typing import Any, Callable

# Third party libraries
import newrelic.agent

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Local libraries

from __init__ import BASE_URL


class CustomRequestMiddleware(BaseHTTPMiddleware):  # type: ignore

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any]
    ) -> Response:
        url = str(request.url)
        traceback = url.split(BASE_URL)[-1]
        if url != traceback:
            newrelic.agent.set_transaction_name(traceback)
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)


class ApiCustomRequestMiddleware(BaseHTTPMiddleware):  # type: ignore

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any]
    ) -> Response:
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)
