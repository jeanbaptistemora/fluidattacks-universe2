# Starlette middlewares file

# Standard library
from collections import defaultdict
from typing import Any, Callable

# Third party libraries
import newrelic.agent
import sqreen

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Local libraries
import back.app.utils as utils

from __init__ import BASE_URL


class CustomRequestMiddleware(BaseHTTPMiddleware):  # type: ignore

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any]
    ) -> Response:
        request = utils.get_starlette_request(request)
        url = str(request.url)
        traceback = url.split(BASE_URL)[-1]
        if url != traceback:
            newrelic.agent.set_transaction_name(traceback)
        request.state.store = defaultdict(lambda: None)
        if request.session.get('username'):
            sqreen.identify({'username': request.session['username']})
        return await call_next(request)
