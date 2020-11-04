# Starlette middlewares file

# Standard library
from collections import defaultdict
from typing import Any, Callable

# Third party libraries
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CustomRequestMiddleware(BaseHTTPMiddleware):  # type: ignore

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any]
    ) -> Response:
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)
