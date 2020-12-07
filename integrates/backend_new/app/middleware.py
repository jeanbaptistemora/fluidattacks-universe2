# Starlette middlewares file

# Standard library
from collections import defaultdict
from typing import Any, Callable

# Third party libraries
import sqreen
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Local libraries
import backend_new.app.utils as utils


class CustomRequestMiddleware(BaseHTTPMiddleware):  # type: ignore

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any]
    ) -> Response:
        request = utils.get_starlette_request(request)
        request.state.store = defaultdict(lambda: None)
        if request.session.get('username'):
            sqreen.identify({'username': request.session['username']})
        return await call_next(request)
