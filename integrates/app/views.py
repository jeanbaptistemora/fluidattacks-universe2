# -*- coding: utf-8 -*-
# Disabling this rule is necessary for include returns inside if-else structure
# pylint: disable-msg=no-else-return
# pylint: disable=too-many-lines
"""Views and services for FluidIntegrates."""

# Third party libraries
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache

# Local libraries
from backend_new import settings


@never_cache  # type: ignore
def index(request: HttpRequest) -> HttpResponse:
    """Login view for unauthenticated users"""
    if 'local' in request.build_absolute_uri(reverse('new')):
        parameters = {'debug': settings.DEBUG}
        return render(request, 'index.html', parameters)

    return HttpResponseRedirect('new/')
