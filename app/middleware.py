from social_django.middleware import SocialAuthExceptionMiddleware
from social_core import exceptions as social_exceptions
from django.http import HttpResponse
from django.shortcuts import redirect

class SocialAuthException(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            exceptionType = exception.__class__.__name__
            if exceptionType == "AuthAlreadyAssociated":
                return HttpResponse('<script> \
                    localStorage.setItem("showAlreadyLoggedin","1"); \
                    if (location.origin.indexOf("://fluidattacks.com") === -1) { \
                        location = "/registration"; \
                    }else{ location = "/integrates/registration"; } </script>')
            elif exceptionType == "AuthCanceled":
                return redirect("/index")
        else:
            return super(SocialAuthException, self).process_exception(request,
                                                                      exception)
