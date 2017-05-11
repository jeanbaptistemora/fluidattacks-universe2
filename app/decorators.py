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
<script>location = "/index"; </script>', status=401)
        return func(*args, **kwargs)
    return authenticate_and_call


def authorize(roles):
    def wrapper(func):
        @functools.wraps(func)
        def authorize_and_call(*args, **kwargs):
            request = args[0]
            if "username" not in request.session or \
                "registered" not in request.session or \
                request.session['role'] not in roles:
                if 'any' not in roles:
                    return HttpResponse('<script>\
alert("No tiene permisos para esto"); </script>')
            return func(*args, **kwargs)
        return authorize_and_call
    return wrapper
