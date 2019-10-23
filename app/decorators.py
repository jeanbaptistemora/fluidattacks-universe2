# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """


import functools
import re

import rollbar
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from graphql import GraphQLError
from promise import Promise
from rediscluster.nodemanager import RedisClusterException

from app import util
from app.exceptions import InvalidAuthorization
from app.services import (
    get_user_role, has_access_to_project, has_access_to_finding,
    has_access_to_event, has_valid_access_token, is_customeradmin
)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs):
        request = args[0]
        if "username" not in request.session or request.session["username"] is None:
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
            if 'username' in request.session and request.session['registered']:
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


# Access control decorators for GraphQL
def verify_csrf(func):
    """
    Conditional CSRF decorator

    Enables django CSRF protection if using cookie-based authentication
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        request = args[0]
        if request.COOKIES.get(settings.JWT_COOKIE_NAME):
            ret = csrf_protect(func)(*args, **kwargs)
        else:
            ret = func(*args, **kwargs)

        if isinstance(ret, Promise):
            ret = ret.get()
        return ret
    return verify_and_call


def require_login(func):
    """
    Require_login decorator

    Verifies that the user is logged in with a valid JWT
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        try:
            user_data = util.get_jwt_content(context)
            if user_data.get('jti'):
                verify_jti(user_data['user_email'],
                           context.META.get('HTTP_AUTHORIZATION'),
                           user_data['jti'])
        except InvalidAuthorization:
            raise GraphQLError('Login required')
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
            role = get_user_role(user_data)
            email = user_data['user_email']

            try:
                if 'customeradmin' in allowed_roles and role == 'customer':
                    project_name = kwargs.get('project_name', args[0].name if args[0] else '')
                    role_customer_admin(project_name, email)
                else:
                    role_allowed(role, allowed_roles)
            except PermissionDenied:
                util.cloudwatch_log(context,
                                    'Security: \
Unauthorized role attempted to perform operation')
                raise GraphQLError('Access denied')
            return func(*args, **kwargs)
        return verify_and_call
    return wrapper


def verify_jti(email, context, jti):
    if not has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


def role_allowed(role, allowed_roles):
    """Is role in allowed_roles."""
    if role not in allowed_roles:
        raise PermissionDenied()


def role_customer_admin(project_name, email):
    if not is_customeradmin(project_name, email):
        raise PermissionDenied()


def require_project_access(func):
    """
    Require_project_access decorator

    Verifies that the current user has access to a given project
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        project_name = kwargs.get('project_name')
        user_data = util.get_jwt_content(context)
        role = get_user_role(user_data)
        if project_name:
            if not has_access_to_project(
                user_data['user_email'],
                project_name,
                role
            ):
                util.cloudwatch_log(context,
                                    'Security: \
Attempted to retrieve {project} project info without permission'
                                    .format(project=kwargs.get('project_name')))
                raise GraphQLError('Access denied')
            util.cloudwatch_log(context,
                                'Security: Access to {project} project'
                                .format(project=kwargs.get('project_name')))
        else:
            rollbar.report_message('Error: Empty fields in project',
                                   'error', context)

        return func(*args, **kwargs)
    return verify_and_call


def require_finding_access(func):
    """
    Require_finding_access decorator.

    Verifies that the current user has access to a given finding
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        finding_id = kwargs.get('finding_id') \
            if kwargs.get('identifier') is None else kwargs.get('identifier')
        user_data = util.get_jwt_content(context)
        role = get_user_role(user_data)

        if not re.match('^[0-9]*$', finding_id):
            rollbar.report_message('Error: Invalid finding id format',
                                   'error', context)
            raise GraphQLError('Invalid finding id format')
        if not has_access_to_finding(user_data['user_email'],
                                     finding_id, role):
            util.cloudwatch_log(context,
                                'Security: \
Attempted to retrieve finding-related info without permission')
            raise GraphQLError('Access denied')
        return func(*args, **kwargs)
    return verify_and_call


def require_event_access(func):
    """
    Require_event_access decorator

    Verifies that the current user has access to a given event
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        event_id = kwargs.get('event_id') \
            if kwargs.get('identifier') is None else kwargs.get('identifier')
        user_data = util.get_jwt_content(context)
        role = get_user_role(user_data)

        if not re.match('^[0-9]*$', event_id):
            rollbar.report_message('Error: Invalid event id format',
                                   'error', context)
            raise GraphQLError('Invalid event id format')
        if not has_access_to_event(
                user_data['user_email'], event_id, role):
            util.cloudwatch_log(context,
                                'Security: \
Attempted to retrieve event-related info without permission')
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
                return ret
            ret = func(*args, **kwargs)
            if isinstance(ret, Promise):
                ret = ret.get()
            cache.set(key_name, ret, timeout=CACHE_TTL)
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return func(*args, **kwargs)
    return decorated


def get_entity_cache(func):
    """Get cached response of a GraphQL entity if it exists."""
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        """Get cached response from function if it exists."""
        gql_ent = args[0]
        uniq_id = str(gql_ent)
        params = '_'.join([kwargs[key] for key in kwargs]) + '_'
        key_name = func.__name__ + '_' + (params if kwargs else '') + uniq_id
        key_name = key_name.lower()
        try:
            ret = cache.get(key_name)
            if ret is None:
                ret = func(*args, **kwargs)
                if isinstance(ret, Promise):
                    ret = ret.get()
                cache.set(key_name, ret, timeout=CACHE_TTL)
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return func(*args, **kwargs)
    return decorated
