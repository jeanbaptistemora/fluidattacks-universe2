# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

import functools
import rollbar
from django.http import HttpResponse
# pylint: disable=E0402
from .services import has_access_to_project
from . import util


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs):
        request = args[0]
        if "username" not in request.session or \
         request.session["username"] is None:
            return HttpResponse('Unauthorized \
            <script>var getUrl=window.location.hash.substr(1); \
            localStorage.setItem("url_inicio",getUrl); \
            location = "/index"; </script>')
        return func(*args, **kwargs)
    return authenticate_and_call


def authorize(roles):
    def wrapper(func):
        @functools.wraps(func)
        def authorize_and_call(*args, **kwargs):
            request = args[0]
            # Verify role if the user is logged in
            if "username" in request.session and \
             request.session['registered'] == '1':
                if request.session['role'] not in roles:
                    return util.response([], 'Access denied', True)

            else:
                # The user is not even authenticated. Redirect to login
                return HttpResponse('<script> \
                               var getUrl=window.location.hash.substr(1); \
                  localStorage.setItem("url_inicio",getUrl); \
                  location = "/index" ; </script>')

            return func(*args, **kwargs)
        return authorize_and_call
    return wrapper

def require_project_access(func):
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        request = args[0]

        if request.method == "POST":
            project = request.POST.get('project', '')
        else:
            project = request.GET.get('project', '')

        project = project.encode('utf-8')
        if project.strip() == "":
            rollbar.report_message('Error: Empty fields in project', 'error', request)
            return util.response([], 'Empty fields', True)
        if not has_access_to_project(request.session['username'], project, request.session['role']):
            rollbar.report_message('Error: Access to project denied', 'error', request)
            return util.response([], 'Access denied', True)
        return func(*args, **kwargs)
    return verify_and_call

def require_finding_access(func):
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        request = args[0]

        if request.method == "POST":
            findingid = request.POST.get('findingid', '')
        else:
            findingid = request.GET.get('findingid', '')

        # Skip this check for admin users since they don't have any assigned projects
        if not request.session['role'] == "admin":
            for project in request.session['access'].keys():
                if findingid in request.session['access'][project]:
                    return func(*args, **kwargs)
            rollbar.report_message('Error: Access to project denied', 'error', request)
            return util.response([], 'Access denied', True)
        return func(*args, **kwargs)
    return verify_and_call
