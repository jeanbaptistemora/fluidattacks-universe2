# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

from datetime import datetime
import asyncio
import functools
import re
from typing import Any, Callable, Dict

import rollbar
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from rediscluster.nodemanager import RedisClusterException
from simpleeval import AttributeDoesNotExist

from backend.dal import finding as finding_dal

from backend.domain import (
    user as user_domain, event as event_domain,
    project as project_domain
)
from backend.services import (
    has_valid_access_token
)

from backend import util
from backend.utils import (
    authorization as authorization_utils
)
from backend.exceptions import InvalidAuthorization

# Constants
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

ENFORCER_PROJECT_ACCESS = getattr(settings, 'ENFORCER_PROJECT_ACCESS')

UNAUTHORIZED_ROLE_MSG = 'Security: Unauthorized role attempted to perform operation'


def authenticate(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs) -> Callable[..., Any]:
        request = args[0]
        if "username" not in request.session or request.session["username"] is None:
            return HttpResponse('Unauthorized \
            <script>var getUrl=window.location.href.split(`${window.location.host}/integrates`);\
            localStorage.setItem("start_url",getUrl[getUrl.length - 1]);\
            location = "/integrates/index"; </script>')
        return func(*args, **kwargs)
    return authenticate_and_call


# Access control decorators for GraphQL
def verify_csrf(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Conditional CSRF decorator

    Enables django CSRF protection if using cookie-based authentication
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        request = args[0]
        if request.COOKIES.get(settings.JWT_COOKIE_NAME):
            ret = csrf_protect(func)(*args, **kwargs)
        else:
            ret = func(*args, **kwargs)
        return ret
    return verify_and_call


def require_login(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Require_login decorator

    Verifies that the user is logged in with a valid JWT
    """
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
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


def resolve_project_name(args, kwargs) -> str:
    """Get project name based on args passed."""
    if args and hasattr(args[0], 'name'):
        project_name = args[0].name
    elif args and hasattr(args[0], 'project_name'):
        project_name = args[0].project_name
    elif args and hasattr(args[0], 'finding_id'):
        project_name = \
            finding_dal.get_attributes(args[0].finding_id, ['project_name']).get('project_name')
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
    elif settings.DEBUG:
        raise Exception('Unable to identify project')
    else:
        project_name = None

    if isinstance(project_name, str):
        project_name = project_name.lower()

    return project_name


def enforce_group_level_auth_async(func: Callable[..., Any]) -> Callable[..., Any]:
    """Enforce authorization using the group-level role."""
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        user_data = util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = resolve_project_name(args, kwargs)
        action = '{}.{}'.format(func.__module__, func.__qualname__).replace('.', '_')

        if not object_:
            rollbar.report_message(
                'Unable to identify project name',
                level='critical',
                extra_data={
                    'subject': subject,
                    'action': action,
                })

        enforcer = authorization_utils.get_group_level_enforcer(subject)

        try:
            if not await enforcer(subject, object_, action):
                util.cloudwatch_log(
                    context, UNAUTHORIZED_ROLE_MSG)
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            util.cloudwatch_log(
                context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def enforce_user_level_auth_async(func: Callable[..., Any]) -> Callable[..., Any]:
    """Enforce authorization using the user-level role."""
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        user_data = util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = 'self'
        action = f'{func.__module__}.{func.__qualname__}'.replace('.', '_')

        enforcer = authorization_utils.get_user_level_enforcer(subject)

        try:
            if not await enforcer(subject, object_, action):
                util.cloudwatch_log(
                    context, UNAUTHORIZED_ROLE_MSG)
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            util.cloudwatch_log(
                context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def verify_jti(email: str, context: Dict[str, str], jti: str) -> None:
    if not has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


def require_project_access(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Require_project_access decorator

    Verifies that the current user has access to a given project
    """
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        context = args[1].context
        project_name = kwargs.get('project_name')

        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']

        user_data['subscribed_projects'] = \
            await sync_to_async(user_domain.get_projects)(user_email)
        user_data['subscribed_projects'] += await \
            sync_to_async(user_domain.get_projects)(user_email, active=False)
        user_data['role'] = await \
            sync_to_async(user_domain.get_group_level_role)(
                user_email, project_name)

        if not project_name:
            await sync_to_async(rollbar.report_message)(
                'Error: Empty fields in project', 'error', context)
            raise GraphQLError('Access denied')
        try:
            if not await sync_to_async(ENFORCER_PROJECT_ACCESS.enforce)(
                    user_data, project_name.lower()):
                util.cloudwatch_log(
                    context, 'Security: Attempted to retrieve '
                    f'{kwargs.get("project_name")} project info '
                    'without permission')
                raise GraphQLError('Access denied')
            util.cloudwatch_log(
                context, 'Security: Access to '
                f'{kwargs.get("project_name")} project')
        except AttributeDoesNotExist:
            return GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def require_finding_access(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Require_finding_access decorator.

    Verifies that the current user has access to a given finding
    """
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        context = args[1].context
        finding_id = kwargs.get('finding_id', '') \
            if kwargs.get('identifier') is None else kwargs.get('identifier')
        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']
        user_data['subscribed_projects'] = \
            await sync_to_async(user_domain.get_projects)(user_email)
        user_data['subscribed_projects'] += await \
            sync_to_async(user_domain.get_projects)(user_email, active=False)
        finding_project = await \
            sync_to_async(project_domain.get_finding_project_name)(finding_id)
        user_data['role'] = \
            await sync_to_async(user_domain.get_group_level_role)(
                user_email, finding_project)

        if not re.match('^[0-9]*$', finding_id):
            await sync_to_async(rollbar.report_message)(
                'Error: Invalid finding id format', 'error', context)
            raise GraphQLError('Invalid finding id format')
        try:
            if not await sync_to_async(ENFORCER_PROJECT_ACCESS.enforce)(
                    user_data, finding_project.lower()):
                util.cloudwatch_log(
                    context, 'Security:  Attempted to retrieve '
                    'finding-related info without permission')
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            return GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def require_event_access(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Require_event_access decorator

    Verifies that the current user has access to a given event
    """
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        context = args[1].context
        event_id = kwargs.get('event_id', '') \
            if kwargs.get('identifier') is None else kwargs.get('identifier')
        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']
        user_data['subscribed_projects'] = \
            await sync_to_async(user_domain.get_projects)(user_email)
        user_data['subscribed_projects'] += await \
            sync_to_async(user_domain.get_projects)(
                user_data['user_email'], active=False)
        event_project = await sync_to_async(event_domain.get_event)(event_id)
        event_project = event_project.get('project_name')
        user_data['role'] = await \
            sync_to_async(user_domain.get_group_level_role)(
                user_email, event_project)

        if not re.match('^[0-9]*$', event_id):
            await sync_to_async(rollbar.report_message)(
                'Error: Invalid event id format', 'error', context)
            raise GraphQLError('Invalid event id format')
        try:
            if not await sync_to_async(ENFORCER_PROJECT_ACCESS.enforce)(
                    user_data, event_project.lower()):
                util.cloudwatch_log(
                    context, 'Security: Attempted to retrieve '
                    'event-related info without permission')
                raise GraphQLError('Access denied')
        except AttributeDoesNotExist:
            return GraphQLError('Access denied: Missing attributes')
        return await func(*args, **kwargs)
    return verify_and_call


def cache_content(func: Callable[..., Any]) -> Callable[..., Any]:
    """Get cached content from a django view with a request object."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Callable[..., Any]:
        """Get cached content from a django view with a request object."""
        req = args[0]
        assert isinstance(req, HttpRequest)
        keys = ['username', 'company', 'findingid', 'project']
        uniq_id = '_'.join([req.session[x] for x in keys if x in req.session])
        uniq_id += '_'.join([req.GET[x] for x in keys if x in req.GET])
        uniq_id += '_'.join([req.POST[x] for x in keys if x in req.POST])
        if len(args) > 1:
            uniq_id += '_'.join([str(x) for x in args[1:]])
        if kwargs:
            uniq_id += '_'.join([str(kwargs[x]) for x in kwargs])
        key_name = \
            f'{func.__module__.replace(".", "_")}_{func.__qualname__}_{uniq_id}'
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


def get_entity_cache_async(func: Callable[..., Any]) -> Callable[..., Any]:
    """Get cached response of a GraphQL entity if it exists."""
    @functools.wraps(func)
    async def decorated(*args, **kwargs) -> Callable[..., Any]:
        """Get cached response from function if it exists."""
        gql_ent = args[0]

        if isinstance(gql_ent, GraphQLResolveInfo):
            uniq_id = '_'.join(
                [key + '_' + str(gql_ent.variable_values[key]) for
                 key in gql_ent.variable_values]
            )
        else:
            uniq_id = str(gql_ent)
        params = '_'.join(
            [str(kwargs[key])
             if not isinstance(kwargs[key], datetime)
             and not isinstance(kwargs[key], list) else str(kwargs[key])[:13]
             for key in kwargs]) + '_'
        complement = (params if kwargs else '') + uniq_id
        key_name = \
            f'{func.__module__.replace(".", "_")}_{func.__qualname__}_{complement}'
        key_name = key_name.lower()
        try:
            ret = await sync_to_async(cache.get)(key_name)
            if ret is None:
                ret = await func(*args, **kwargs)
                cache_set_coro = \
                    sync_to_async(cache.set)(key_name, ret, timeout=CACHE_TTL)
                asyncio.create_task(cache_set_coro)
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return func(*args, **kwargs)
    return decorated


def rename_kwargs(mapping: Dict[str, str]) -> Callable[..., Any]:
    """Decorator to rename function's kwargs.

    Useful to perform breaking changes,
    with backwards compatibility.
    """

    def wrapped(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def decorated(*args, **kwargs) -> Callable[..., Any]:
            kwargs = {
                mapping.get(key, key): val
                for key, val in kwargs.items()
            }
            return func(*args, **kwargs)

        return decorated

    return wrapped
