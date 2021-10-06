# Starlette middlewares file


from collections import (
    defaultdict,
)
from context import (
    BASE_URL,
)
import newrelic.agent
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)
from typing import (
    Any,
    Callable,
)


class CustomRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[..., Any]
    ) -> Response:
        url = str(request.url)
        traceback = url.split(BASE_URL)[-1]  # pylint: disable=use-maxsplit-arg
        if url != traceback:
            newrelic.agent.set_transaction_name(traceback)
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)


class ApiCustomRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[..., Any]
    ) -> Response:
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)
