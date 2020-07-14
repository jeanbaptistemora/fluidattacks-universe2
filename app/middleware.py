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
                    'location.assign("/integrates/registration");</script>'
                )
            return redirect('/integrates/index')
        return super(SocialAuthException, self).process_exception(
            request, exception
        )
