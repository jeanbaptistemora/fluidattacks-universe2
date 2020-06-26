# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

from datetime import datetime
import functools
import inspect
import re
from typing import Any, Callable, Dict, cast

import rollbar
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from frozendict import frozendict
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from rediscluster.nodemanager import RedisClusterException

from backend.domain import (
    user as user_domain,
    event as event_domain,
    finding as finding_domain
)
from backend.services import (
    has_valid_access_token
)
from backend import authz, util
from backend.exceptions import (
    InvalidAuthorization,
    FindingNotFound
)
from backend.utils import (
    aio,
    apm,
)

# Constants
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

UNAUTHORIZED_ROLE_MSG = (
    'Security: Unauthorized role '
    'attempted to perform operation'
)


def authenticate(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def authenticate_and_call(*args, **kwargs) -> Callable[..., Any]:
        request = args[0]
        if "username" not in request.session or \
                request.session["username"] is None:
            return HttpResponse(
                'Unauthorized '
                '<script>var getUrl=window.location.href'
                '.split(`${window.location.host}/integrates`); '
                'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
                'location = "/integrates/index"; </script>'
            )
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

    @apm.trace(display_name='require_login')
    @functools.wraps(func)
    def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        # The underlying request object being served
        context = args[1].context if len(args) > 1 else args[0]

        try:
            user_data = util.get_jwt_content(context)
            if util.is_api_token(user_data):
                verify_jti(
                    user_data['user_email'],
                    context.META.get('HTTP_AUTHORIZATION'),
                    user_data['jti']
                )
        except InvalidAuthorization:
            raise GraphQLError('Login required')
        return func(*args, **kwargs)
    return verify_and_call


async def resolve_project_name(args, kwargs) -> str:  # noqa: MC0001
    """Get project name based on args passed."""
    if args and hasattr(args[0], 'name'):
        project_name = args[0].name
    elif args and hasattr(args[0], 'project_name'):
        project_name = args[0].project_name
    elif args and hasattr(args[0], 'finding_id'):
        project_name = await finding_domain.get_project(args[0].finding_id)
    elif 'project_name' in kwargs:
        project_name = kwargs['project_name']
    elif 'group_name' in kwargs:
        project_name = kwargs['group_name']
    elif 'finding_id' in kwargs:
        project_name = await finding_domain.get_project(kwargs['finding_id'])
    elif 'draft_id' in kwargs:
        project_name = await finding_domain.get_project(kwargs['draft_id'])
    elif 'event_id' in kwargs:
        event = await sync_to_async(event_domain.get_event)(
            kwargs['event_id'])
        project_name = event.get('project_name')
    elif settings.DEBUG:
        raise Exception('Unable to identify project')
    else:
        project_name = None

    if isinstance(project_name, str):
        project_name = project_name.lower()

    return project_name


def enforce_group_level_auth_async(func: Callable[..., Any]) -> \
        Callable[..., Any]:
    """Enforce authorization using the group-level role."""

    @apm.trace(display_name='enforce_group_level_auth_async')
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
        object_ = await resolve_project_name(args, kwargs)
        action = f'{func.__module__}.{func.__qualname__}'.replace('.', '_')

        if not object_:
            rollbar.report_message(
                'Unable to identify project name',
                level='critical',
                extra_data={
                    'subject': subject,
                    'action': action,
                }
            )

        enforcer = authz.get_group_level_enforcer(subject)

        if not await enforcer(subject, object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def enforce_user_level_auth_async(func: Callable[..., Any]) -> \
        Callable[..., Any]:
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

        enforcer = authz.get_user_level_enforcer(subject)

        if not await enforcer(subject, object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def verify_jti(email: str, context: Dict[str, str], jti: str) -> None:
    if not has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


def require_attribute(attribute: str):

    def wrapper(function: Callable) -> Callable:

        @apm.trace(display_name='require_attribute')
        @functools.wraps(function)
        async def resolve_and_call(*args, **kwargs):
            group = await resolve_project_name(args, kwargs)

            enforcer = authz.get_group_service_attributes_enforcer(group)

            if not await enforcer(attribute):
                raise GraphQLError('Access denied')

            return await function(*args, **kwargs)

        return resolve_and_call

    return wrapper


def require_integrates(function: Callable) -> Callable:
    return require_attribute('has_integrates')(function)


def require_project_access(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Require_project_access decorator

    Verifies that the current user has access to a given project
    """

    @apm.trace(display_name='require_project_access')
    @functools.wraps(func)
    async def verify_and_call(*args, **kwargs) -> Callable[..., Any]:
        context = args[1].context
        project_name = kwargs.get('project_name') or kwargs.get('group_name')

        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']

        user_data['subscribed_projects'] = cast(
            str,
            await user_domain.get_projects(user_email)
        )
        user_data['subscribed_projects'] += cast(
            str,
            await user_domain.get_projects(user_email, active=False)
        )
        user_data['role'] = await sync_to_async(authz.get_group_level_role)(
            user_email, project_name)

        if not project_name:
            await sync_to_async(rollbar.report_message)(
                'Error: Empty fields in project', 'error', context)
            raise GraphQLError('Access denied')

        enforcer = authz.get_group_access_enforcer()

        if not await enforcer(user_data, project_name):
            util.cloudwatch_log(
                context,
                'Security: Attempted to retrieve '
                f'{kwargs.get("project_name")} project info '
                'without permission'
            )
            raise GraphQLError('Access denied')
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
        finding_id = (
            kwargs.get('finding_id', '')
            if kwargs.get('identifier') is None
            else kwargs.get('identifier')
        )
        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']
        user_data['subscribed_projects'] = cast(
            str,
            await user_domain.get_projects(user_email)
        )
        user_data['subscribed_projects'] += cast(
            str,
            await user_domain.get_projects(user_email, active=False)
        )
        finding_project = await finding_domain.get_project(finding_id)
        user_data['role'] = await sync_to_async(
            authz.get_group_level_role)(user_email, finding_project)

        if not re.match('^[0-9]*$', finding_id):
            await sync_to_async(rollbar.report_message)(
                'Error: Invalid finding id format',
                'error',
                context
            )
            raise GraphQLError('Invalid finding id format')

        enforcer = authz.get_group_access_enforcer()

        if not finding_domain.validate_finding(finding_id):
            raise FindingNotFound()

        if not await enforcer(user_data, finding_project):
            util.cloudwatch_log(
                context,
                'Security:  Attempted to retrieve '
                'finding-related info without permission'
            )
            raise GraphQLError('Access denied')
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
        event_id = (
            kwargs.get('event_id', '')
            if kwargs.get('identifier') is None
            else kwargs.get('identifier')
        )
        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']
        user_data['subscribed_projects'] = cast(
            str,
            await user_domain.get_projects(user_email)
        )
        user_data['subscribed_projects'] += cast(
            str,
            await user_domain.get_projects(
                user_data['user_email'],
                active=False
            )
        )
        event_project = await sync_to_async(event_domain.get_event)(event_id)
        event_project = event_project.get('project_name')
        user_data['role'] = await sync_to_async(authz.get_group_level_role)(
            user_email, event_project)

        if not re.match('^[0-9]*$', event_id):
            await sync_to_async(rollbar.report_message)(
                'Error: Invalid event id format', 'error', context)
            raise GraphQLError('Invalid event id format')

        enforcer = authz.get_group_access_enforcer()

        if not await enforcer(user_data, event_project):
            util.cloudwatch_log(
                context,
                'Security: Attempted to retrieve '
                'event-related info without permission'
            )
            raise GraphQLError('Access denied')
        return await func(*args, **kwargs)
    return verify_and_call


def cache_content(func: Callable[..., Any]) -> Callable[..., Any]:
    """Get cached content from a django view with a request object."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Callable[..., Any]:
        """Get cached content from a django view with a request object."""
        req = args[0]
        assert isinstance(req, HttpRequest)
        keys = [
            'username',
            'company',
            'findingid',
            'project',
            'documentName',
            'documentType',
            'entity',
            'generatorName',
            'generatorType',
            'height',
            'subject',
            'width',
        ]
        uniq_id = '_'.join([
            req.session[x]
            for x in keys
            if x in req.session
        ])
        uniq_id += '_'.join([
            req.GET[x]
            for x in keys
            if x in req.GET
        ])
        uniq_id += '_'.join([
            req.POST[x]
            for x in keys
            if x in req.POST
        ])
        if len(args) > 1:
            uniq_id += '_'.join([
                str(x)
                for x in args[1:]
            ])
        if kwargs:
            uniq_id += '_'.join([
                str(kwargs[x])
                for x in kwargs
            ])
        key_name = (
            f'{func.__module__.replace(".", "_")}_'
            f'{func.__qualname__}_{uniq_id}'
        )
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

    @apm.trace(display_name='get_entity_cache_async')
    @functools.wraps(func)
    async def decorated(*args, **kwargs) -> Callable[..., Any]:
        """Get cached response from function if it exists."""
        gql_ent = args[0]

        if isinstance(gql_ent, GraphQLResolveInfo):
            uniq_id = '_'.join([
                key + '_' + str(gql_ent.variable_values[key])
                for key in gql_ent.variable_values
            ])
        else:
            uniq_id = str(gql_ent)
        params = '_'.join([
            str(kwargs[key])
            if not isinstance(kwargs[key], datetime) and
            not isinstance(kwargs[key], list)
            else str(kwargs[key])[:13]
            for key in kwargs
        ]) + '_'
        complement = (params if kwargs else '') + uniq_id
        key_name = (
            f'{func.__module__.replace(".", "_")}_'
            f'{func.__qualname__}_{complement}'
        )
        key_name = key_name.lower()
        try:
            ret = await aio.ensure_io_bound(
                aio.PyCallable(
                    instance=cache.get,
                    args=(key_name,),
                )
            )

            if ret is None:
                ret = await func(*args, **kwargs)

                await aio.ensure_io_bound(
                    aio.PyCallable(
                        instance=cache.set,
                        args=(key_name, ret),
                        kwargs=frozendict(timeout=CACHE_TTL)
                    )
                )
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return await func(*args, **kwargs)

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


def cache_idempotent(function: Callable) -> Callable:

    @apm.trace(display_name='get_entity_cache_async')
    @functools.wraps(function)
    async def wrapper(*args, **kwargs) -> Callable[..., Any]:
        signature = inspect.signature(function).bind(*args, **kwargs)

        cache_key = (
            f'{function.__module__}.{function.__qualname__}:' +
            ''.join(f'{arg}_{val}' for arg, val in signature.arguments.items())
        )

        try:
            ret = await aio.ensure_io_bound(
                aio.PyCallable(
                    instance=cache.get,
                    args=(cache_key,),
                )
            )

            if ret is None:
                ret = await function(*args, **kwargs)

                await aio.ensure_io_bound(
                    aio.PyCallable(
                        instance=cache.set,
                        args=(cache_key, ret),
                        kwargs=frozendict(timeout=CACHE_TTL)
                    )
                )
            return ret
        except RedisClusterException:
            rollbar.report_exc_info()
            return await function(*args, **kwargs)

    return wrapper


def turn_args_into_kwargs(function: Callable):
    """Turn function's positional-arguments into keyword-arguments.

    Very useful when you want to keep an strongly typed signature in your
    function while using another decorators from this module that work on
    keyword arguments only for backwards compatibility reasons.

    This avoids functions with a typeless **parameters, and then 50 lines
    unpacking the arguments and casting them to the expected types.
    """
    @functools.wraps(function)
    async def new_function(*args, **kwargs):
        # The first two arguments are django's self, and info references
        #   They can be safely left intact

        args_as_kwargs = dict(zip(
            inspect.getfullargspec(function).args[2:], args[2:]
        ))

        return await function(*args[0:2], **args_as_kwargs, **kwargs)

    return new_function
