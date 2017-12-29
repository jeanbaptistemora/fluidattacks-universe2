# -*- coding: utf-8 -*-
"""
    Decoradores para FluidIntegrates
"""

import functools
from django.http import HttpResponse


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs):
        request = args[0]
        if "username" in request.session:
            if request.session["username"] is None:
                return HttpResponse('Unauthorized \
                <script>var getUrl=window.location.hash.substr(1); \
                localStorage.setItem("url_inicio",getUrl); \
                location = "/logout"; </script>', status=401)
        return func(*args, **kwargs)
    return authenticate_and_call


def authorize(roles):
    def wrapper(func):
        @functools.wraps(func)
        def authorize_and_call(*args, **kwargs):
            request = args[0]
            if "username" not in request.session or \
                request.session['registered'] != '1' or \
                request.session['role'] not in roles:
                if 'any' not in roles:
                    return HttpResponse('<script> \
                           var getUrl=window.location.hash.substr(1); \
              localStorage.setItem("url_inicio",getUrl); \
              location = window.location.href.split("/dashboard")[0] ; </script>')
            return func(*args, **kwargs)
        return authorize_and_call
    return wrapper
