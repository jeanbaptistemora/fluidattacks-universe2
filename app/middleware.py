from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from social_core import exceptions as social_exceptions
from social_django.middleware import SocialAuthExceptionMiddleware

from app.exceptions import ForbiddenField


class SocialAuthException(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            exception_type = exception.__class__.__name__

            # An already logged in user attempted to access with a different account
            if exception_type == "AuthAlreadyAssociated":
                return HttpResponse('<script> \
                    localStorage.setItem("showAlreadyLoggedin","1"); \
                    if (location.origin.indexOf("://fluidattacks.com") === -1) { \
                        location = "/registration"; \
                    }else{ location = "/integrates/registration"; } </script>')

            # A user clicked return or stopped the page load after social auth
            elif exception_type in ["AuthCanceled", "AuthMissingParameter",
                                    "AuthStateMissing"]:
                return redirect("/index")
        else:
            return super(SocialAuthException, self).process_exception(request,
                                                                      exception)


def graphql_blacklist_middleware(next_middleware, root, info, **kwargs):
    blacklisted_fields = ['__schema', '__type']
    if info.field_name.lower() in blacklisted_fields \
            and not settings.DEBUG:
        raise ForbiddenField()
    return next_middleware(root, info, **kwargs)
