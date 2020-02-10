# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """


import functools
import re

import rollbar
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from graphql import GraphQLError
from promise import Promise
from rediscluster.nodemanager import RedisClusterException
from simpleeval import AttributeDoesNotExist

from backend.dal import finding as finding_dal, project as project_dal

from backend.domain import (
    user as user_domain, event as event_domain, finding as finding_domain
)
from backend.services import (
    get_user_role, has_valid_access_token, project_exists
)

from backend import util
from backend.exceptions import InvalidAuthorization

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

ENFORCER_BASIC = getattr(settings, 'ENFORCER_BASIC')
ENFORCER_ACTION = getattr(settings, 'ENFORCER_ACTION')


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs):
        request = args[0]
        if "username" not in request.session or request.session["username"] is None:
            return HttpResponse('Unauthorized \
            <script>var getUrl=window.location.hash.substr(1); \
            localStorage.setItem("url_inicio",getUrl); \
            location = "/integrates/index"; </script>')
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
                  location = "/integrates/index" ; </script>')

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


def resolve_project_name(args, kwargs):
    """Get project name based on args passed."""
    if args[0] and hasattr(args[0], 'name'):
        project_name = args[0].name
    elif 'project_name' in kwargs:
        project_name = kwargs['project_name']
    elif 'finding_id' in kwargs:
        project_name = \
            finding_dal.get_attributes(kwargs['finding_id'], ['project_name']).get('project_name')
    elif 'draft_id' in kwargs:
        project_name = \
            finding_dal.get_attributes(kwargs['draft_id'], ['project_name']).get('project_name')
    elif 'event_id' in kwargs:
        project_name = \
            event_domain.get_event(kwargs['event_id']).get('project_name')
    else:
        project_name = None
    return project_name


def resolve_project_data(project_name):
    """Get project data or mock it if needed."""
    if project_name:
        if not project_exists(project_name):
            project_data = {}
        else:
            project_data = project_dal.get(project_name)[0]
    else:
        project_data = {}

    if 'customeradmin' not in project_data:
        project_data['customeradmin'] = set()
    return project_data


def new_require_role(func):
    """
    Require_role decorator based on Casbin enforcer.

    Verifies that the current user's role is within the specified allowed roles
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs):
        context = args[1].context
        user_data = util.get_jwt_content(context)
        user_data['role'] = get_user_role(user_data)
        project_name = resolve_project_name(args, kwargs)
        project_data = resolve_project_data(project_name)
        action = '{}.{}'.format(func.__module__, func.__qualname__)
        action = action.replace('.', '_')
        try:
            if not ENFORCER_ACTION.enforce(user_data, project_data, action):
                util.cloudwatch_log(context,
                                    'Security: \
Unauthorized role attempted to perform operation')
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            util.cloudwatch_log(context,
                                'Security: \
Unauthorized role attempted to perform operation')
            raise GraphQLError('Access denied')
        return func(*args, **kwargs)
    return verify_and_call


def verify_jti(email, context, jti):
    if not has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


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
        user_data['subscribed_projects'] = \
            user_domain.get_projects(user_data['user_email'])
        user_data['subscribed_projects'] += \
            user_domain.get_projects(user_data['user_email'], active=False)
        user_data['role'] = get_user_role(user_data)
        if not project_name:
            rollbar.report_message('Error: Empty fields in project',
                                   'error', context)
            raise GraphQLError('Access denied')
        try:
            if not ENFORCER_BASIC.enforce(user_data, project_name.lower()):
                util.cloudwatch_log(context,
                                    'Security: \
Attempted to retrieve {project} project info without permission'
                                    .format(project=kwargs.get('project_name')))
                raise GraphQLError('Access denied')
            util.cloudwatch_log(context,
                                'Security: Access to {project} project'
                                .format(project=kwargs.get('project_name')))
        except AttributeDoesNotExist:
            return GraphQLError('Access denied')
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
        user_data['subscribed_projects'] = \
            user_domain.get_projects(user_data['user_email'])
        user_data['subscribed_projects'] += \
            user_domain.get_projects(user_data['user_email'], active=False)
        user_data['role'] = get_user_role(user_data)
        finding_project = finding_domain.get_finding(finding_id).get('projectName')

        if not re.match('^[0-9]*$', finding_id):
            rollbar.report_message('Error: Invalid finding id format',
                                   'error', context)
            raise GraphQLError('Invalid finding id format')
        try:
            if not ENFORCER_BASIC.enforce(user_data, finding_project.lower()):
                util.cloudwatch_log(context,
                                    'Security: \
    Attempted to retrieve finding-related info without permission')
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            return GraphQLError('Access denied')
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
        user_data['subscribed_projects'] = \
            user_domain.get_projects(user_data['user_email'])
        user_data['subscribed_projects'] += \
            user_domain.get_projects(user_data['user_email'], active=False)
        user_data['role'] = get_user_role(user_data)
        event_project = event_domain.get_event(event_id).get('project_name')

        if not re.match('^[0-9]*$', event_id):
            rollbar.report_message('Error: Invalid event id format',
                                   'error', context)
            raise GraphQLError('Invalid event id format')
        try:
            if not ENFORCER_BASIC.enforce(user_data, event_project.lower()):
                util.cloudwatch_log(context,
                                    'Security: \
    Attempted to retrieve event-related info without permission')
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            return GraphQLError('Access denied: Missing attributes')
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
        uniq_id = "_".join([str(kwargs[x])[:24] for x in kwargs])
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
