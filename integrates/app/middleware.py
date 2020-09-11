# Standard library
from collections import defaultdict
from typing import (
    Any,
    Callable,
)

# Third party libraries
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from social_core import exceptions as social_exceptions
from social_django.middleware import SocialAuthExceptionMiddleware


class SocialAuthException(SocialAuthExceptionMiddleware):  # type: ignore
    def process_exception(
        self,
        request: HttpRequest,
        exception: social_exceptions.SocialAuthBaseException
    ) -> HttpResponse:
        if hasattr(social_exceptions, exception.__class__.__name__):
            exception_type = exception.__class__.__name__

            # An already logged in user attempted to
            # access with a different account
            if exception_type == 'AuthAlreadyAssociated':
                return HttpResponse(
                    '<script> '
                    'localStorage.setItem("showAlreadyLoggedin","1"); '
                    'location.assign("/registration");</script>'
                )
            return redirect('/')
        return super(SocialAuthException, self).process_exception(
            request, exception
        )


def request_lifespan_store(next_in_chain: Callable[..., Any]) -> Any:
    """Middleware to add a `defaultdict` into the request object.

    After the middleware is applied `request.store` can be used to store
    values with a lifetime of the request itself.

    Data is not shared across requests.
    """

    def middleware(request: HttpRequest) -> HttpResponse:
        # Append the request store as an attribute
        request.store = defaultdict(lambda: None)

        return next_in_chain(request)

    return middleware
