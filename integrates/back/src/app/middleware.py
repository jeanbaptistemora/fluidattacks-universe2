# Starlette middlewares file


from collections import (
    defaultdict,
)
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
        request.state.store = defaultdict(lambda: None)
        return await call_next(request)
