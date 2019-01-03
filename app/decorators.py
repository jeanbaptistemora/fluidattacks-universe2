# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

import functools
import re

import rollbar
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from graphql import GraphQLError

# pylint: disable=E0402
from .services import has_access_to_project, has_access_to_finding, is_customeradmin
from . import util
from rediscluster.nodemanager import RedisClusterException


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


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
            util.cloudwatch_log(request, 'Security: Attempted to retrieve project info without permission')
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

        if not re.match("^[0-9]*$", findingid):
            rollbar.report_message('Error: Invalid finding id format', 'error', request)
            return util.response([], 'Invalid finding id format', True)
        if not has_access_to_finding(request.session['username'], findingid, request.session['role']):
            util.cloudwatch_log(request, 'Security: Attempted to retrieve finding-related info without permission')
            return util.response([], 'Access denied', True)
        return func(*args, **kwargs)
    return verify_and_call


# Access control decorators for GraphQL
def require_login(func):
    """
    Require_login decorator

    Verifies that the user is logged in with a valid JWT
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        token = context.COOKIES.get(settings.JWT_COOKIE_NAME)
        if not token:
            raise GraphQLError('Login required')
        else:
            pass
        return func(*args, **kwargs)
    return verify_and_call


def require_role(allowed_roles):
    """
    Require_role decorator

    Verifies that the current user's role is within the specified allowed roles
    """
    def wrapper(func):
        @functools.wraps(func)
        def verify_and_call(*args, **kwargs):
            context = args[1].context
            user_data = util.get_jwt_content(context)
            role = user_data['user_role']
            email = user_data['user_email']

            try:
                if 'customeradmin' in allowed_roles and role == 'customer':
                    project_name = kwargs.get('project_name')
                    if not is_customeradmin(project_name, email):
                        raise PermissionDenied()
                    else:
                        pass
                else:
                    if role not in allowed_roles:
                        raise PermissionDenied()
                    else:
                        pass
            except PermissionDenied:
                util.cloudwatch_log(context,
                    'Security: Unauthorized role attempted to perform operation')
                raise GraphQLError('Access denied')
            return func(*args, **kwargs)
        return verify_and_call
    return wrapper


def require_project_access_gql(func):
    """
    Require_project_access decorator

    Verifies that the current user has access to a given project
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        project_name = kwargs.get('project_name')
        user_data = util.get_jwt_content(context)
        if project_name:
            if not has_access_to_project(
                user_data['user_email'],
                project_name,
                user_data['user_role']
            ):
                util.cloudwatch_log(context,
                    'Security: Attempted to retrieve project info without permission')
                raise GraphQLError('Access denied')
            else:
                pass
        else:
            rollbar.report_message('Error: Empty fields in project', 'error', context)

        return func(*args, **kwargs)
    return verify_and_call


def require_finding_access_gql(func):
    """
    Require_finding_access decorator

    Verifies that the current user has access to a given finding
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        finding_id = kwargs.get('finding_id') if kwargs.get('identifier') is None else kwargs.get('identifier')
        user_data = util.get_jwt_content(context)

        if not re.match('^[0-9]*$', finding_id):
            rollbar.report_message('Error: Invalid finding id format', 'error', context)
            raise GraphQLError('Invalid finding id format')
        if not has_access_to_finding(user_data['user_email'], finding_id, user_data['user_role']):
            util.cloudwatch_log(context,
                'Security: Attempted to retrieve finding-related info without permission')
            raise GraphQLError('Access denied')
        return func(*args, **kwargs)
    return verify_and_call


def cache_content(func):
    """Get cached content from a django view with a request object."""
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        """Get cached content from a django view with a request object."""
        req = args[0]
        assert isinstance(req, HttpRequest)
        keys = ['username', 'company', 'role', 'findingid', 'project']
        uniq_id = '_'.join([req.session[x] for x in keys if x in req.session])
        uniq_id += '_'.join([req.GET[x] for x in keys if x in req.GET])
        uniq_id += '_'.join([req.POST[x] for x in keys if x in req.POST])
        if len(args) > 1:
            uniq_id += '_'.join([str(x) for x in args[1:]])
        if kwargs:
            uniq_id += '_'.join([str(kwargs[x]) for x in kwargs])
        key_name = func.__name__ + '_' + uniq_id
        key_name = key_name.lower()
        try:
            ret = cache.get(key_name)
            if ret:
                cache.touch(key_name, CACHE_TTL)
                return ret
            ret = func(*args, **kwargs)
            cache.set(key_name, ret, timeout=CACHE_TTL)
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return func(*args, **kwargs)
    return decorated


def get_cached(func):
    """Get cached response from function if it exists."""
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        """Get cached response from function if it exists."""
        uniq_id = "_".join([str(kwargs[x])[:12] for x in kwargs])
        key_name = func.__name__ + '_' + uniq_id
        key_name = key_name.lower()
        try:
            ret = cache.get(key_name)
            if ret:
                cache.touch(key_name, CACHE_TTL)
                return ret
            ret = func(*args, **kwargs)
            cache.set(key_name, ret, timeout=CACHE_TTL)
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return func(*args, **kwargs)
    return decorated
