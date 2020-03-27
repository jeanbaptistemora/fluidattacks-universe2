from django.http import HttpResponse
from django.shortcuts import redirect
from social_core import exceptions as social_exceptions
from social_django.middleware import SocialAuthExceptionMiddleware


class SocialAuthException(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            exception_type = exception.__class__.__name__

            # An already logged in user attempted to access with a different account
            if exception_type == 'AuthAlreadyAssociated':
                return HttpResponse('<script> \
                    localStorage.setItem("showAlreadyLoggedin","1"); \
                    location.assign("/integrates/registration");</script>')
            return redirect("/integrates/index")
        return super(SocialAuthException, self).process_exception(request,
                                                                  exception)
