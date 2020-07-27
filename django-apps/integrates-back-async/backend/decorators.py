# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

import asyncio
from datetime import datetime
import functools
import inspect
import logging
import re
from typing import Any, Callable, Dict, cast, TypeVar

from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from rediscluster.nodemanager import RedisClusterException

from backend.domain import (
    event as event_domain,
    finding as finding_domain,
    organization as org_domain
)
from backend.services import (
    has_valid_access_token
)
from backend import authz, util
from backend.exceptions import (
    FindingNotFound,
    InvalidAuthorization,
    UserNotInOrganization
)
from backend.utils import (
    aio,
    apm,
)

# Constants
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
LOGGER = logging.getLogger(__name__)
TVar = TypeVar('TVar')

UNAUTHORIZED_ROLE_MSG = (
    'Security: Unauthorized role '
    'attempted to perform operation'
)


def authenticate(func: TVar) -> TVar:

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    def authenticate_and_call(*args: Any, **kwargs: Any) -> Any:
        request = args[0]
        if ("username" not in request.session or
                request.session["username"] is None):
            parameters: Dict[str, str] = dict()
            return render(request, 'unauthorized.html', parameters)
        return _func(*args, **kwargs)
    return cast(TVar, authenticate_and_call)


# Access control decorators for GraphQL
def verify_csrf(func: TVar) -> TVar:
    """
    Conditional CSRF decorator

    Enables django CSRF protection if using cookie-based authentication
    """

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        request = args[0]
        if request.COOKIES.get(settings.JWT_COOKIE_NAME):
            ret = csrf_protect(func)(*args, **kwargs)
        else:
            ret = _func(*args, **kwargs)
        return ret
    return cast(TVar, verify_and_call)


def require_login(func: TVar) -> TVar:
    """
    Require_login decorator

    Verifies that the user is logged in with a valid JWT
    """

    _func = cast(Callable[..., Any], func)

    @apm.trace(overridden_function=require_login)
    @functools.wraps(_func)
    def verify_and_call(*args: Any, **kwargs: Any) -> Any:
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
        return _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


async def resolve_project_name(args: Any, kwargs: Any) -> str:  # noqa: MC0001
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
        event = await event_domain.get_event(
            kwargs['event_id'])
        project_name = event.get('project_name')
    elif settings.DEBUG:
        raise Exception('Unable to identify project')
    else:
        project_name = ''

    if isinstance(project_name, str):
        project_name = project_name.lower()

    return cast(str, project_name)


def enforce_group_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the group-level role."""

    _func = cast(Callable[..., Any], func)

    @apm.trace(overridden_function=enforce_group_level_auth_async)
    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        user_data = util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = await resolve_project_name(args, kwargs)
        action = f'{_func.__module__}.{_func.__qualname__}'.replace('.', '_')

        if not object_:
            LOGGER.error(
                'Unable to identify project name',
                extra={
                    'extra': {
                        'action': action,
                        'subject': subject,
                    }
                })

        enforcer = await aio.ensure_io_bound(
            authz.get_group_level_enforcer,
            subject
        )

        if not await enforcer(subject, object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


def enforce_organization_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the organization-level role."""

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        organization_identifier = str(
            kwargs.get('identifier') or
            kwargs.get('organization_id') or
            kwargs.get('organization_name')
        )
        organization_id = (
            organization_identifier
            if organization_identifier.startswith('ORG#')
            else await org_domain.get_id_by_name(organization_identifier)
        )
        user_data = util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = organization_id.lower()
        action = f'{_func.__module__}.{_func.__qualname__}'.replace('.', '_')

        if not object_:
            LOGGER.error(
                'Unable to identify organization to check permissions',
                extra={
                    'action': action,
                    'subject': subject,
                })

        enforcer = await aio.ensure_io_bound(
            authz.get_organization_level_enforcer,
            subject
        )

        if not await enforcer(subject, object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


def enforce_user_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the user-level role."""

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        user_data = util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = 'self'
        action = f'{_func.__module__}.{_func.__qualname__}'.replace('.', '_')

        enforcer = await aio.ensure_io_bound(
            authz.get_user_level_enforcer,
            subject
        )

        if not await enforcer(subject, object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


def verify_jti(email: str, context: Dict[str, str], jti: str) -> None:
    if not has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


def require_attribute(attribute: str) -> Callable[[TVar], TVar]:

    def wrapper(func: TVar) -> TVar:

        _func = cast(Callable[..., Any], func)

        @apm.trace(overridden_function=require_attribute)
        @functools.wraps(_func)
        async def resolve_and_call(*args: Any, **kwargs: Any) -> Any:
            group = await resolve_project_name(args, kwargs)

            enforcer = authz.get_group_service_attributes_enforcer(group)

            if not await enforcer(attribute):
                raise GraphQLError('Access denied')

            return await _func(*args, **kwargs)

        return cast(TVar, resolve_and_call)

    return wrapper


def require_integrates(func: TVar) -> TVar:
    return require_attribute('has_integrates')(func)


def require_organization_access(func: TVar) -> TVar:
    """
    Decorator
    Verifies that the user trying to fetch information belongs to the
    organization
    """

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        organization_identifier = str(
            kwargs.get('identifier') or
            kwargs.get('organization_id') or
            kwargs.get('organization_name')
        )

        user_data = util.get_jwt_content(context)
        user_email = user_data['user_email']

        organization_id = (
            organization_identifier
            if organization_identifier.startswith('ORG#')
            else await org_domain.get_id_by_name(organization_identifier)
        )

        role = await sync_to_async(authz.get_organization_level_role)(
            user_email, organization_id)
        has_access = await org_domain.has_user_access(
            user_email, organization_id
        )

        if role != 'admin' and not has_access:
            util.cloudwatch_log(
                context,
                f'Security: User {user_email} attempted to access '
                f'organization {organization_identifier} without permission'
            )
            raise UserNotInOrganization()
        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


def require_finding_access(func: TVar) -> TVar:
    """
    Require_finding_access decorator.

    Verifies that the current user has access to a given finding
    """

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        context = args[1].context
        finding_id = (
            kwargs.get('finding_id', '')
            if kwargs.get('identifier') is None
            else kwargs.get('identifier')
        )

        if not re.match('^[0-9]*$', finding_id):
            LOGGER.error(
                'Invalid finding id format',
                extra={'extra': {'context': context}})

            raise GraphQLError('Invalid finding id format')

        if not await finding_domain.validate_finding(finding_id):
            raise FindingNotFound()

        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


def cache_content(func: TVar) -> TVar:
    """Get cached content from a django view with a request object."""

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        """Get cached content from a django view with a request object."""
        req = args[0]
        assert isinstance(req, HttpRequest)
        keys = [
            'username',
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
            f'{_func.__module__.replace(".", "_")}_'
            f'{_func.__qualname__}_{uniq_id}'
        )
        try:
            ret = cache.get(key_name)
            if ret:
                return ret
            ret = _func(*args, **kwargs)
            cache.set(key_name, ret, timeout=CACHE_TTL)
            return ret
        except RedisClusterException as ex:
            LOGGER.exception(ex)
            return _func(*args, **kwargs)
    return cast(TVar, decorated)


def get_entity_cache_async(func: TVar) -> TVar:
    """Get cached response of a GraphQL entity if it exists."""

    _func = cast(Callable[..., Any], func)

    @apm.trace(overridden_function=get_entity_cache_async)
    @functools.wraps(_func)
    async def decorated(*args: Any, **kwargs: Any) -> Any:
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
            f'{_func.__module__.replace(".", "_")}_'
            f'{_func.__qualname__}_{complement}'
        )
        key_name = key_name.lower()
        try:
            ret = await aio.ensure_io_bound(cache.get, key_name)

            if ret is None:
                ret = await _func(*args, **kwargs)

                await aio.ensure_io_bound(
                    cache.set, key_name, ret, timeout=CACHE_TTL,
                )
            return ret
        except RedisClusterException as ex:
            LOGGER.exception(ex)
            return await _func(*args, **kwargs)

    return cast(TVar, decorated)


def rename_kwargs(mapping: Dict[str, str]) -> Callable[[TVar], TVar]:
    """Decorator to rename function's kwargs.

    Useful to perform breaking changes,
    with backwards compatibility.
    """

    def wrapped(func: TVar) -> TVar:

        _func = cast(Callable[..., Any], func)

        @functools.wraps(_func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            kwargs = {
                mapping.get(key, key): val
                for key, val in kwargs.items()
            }
            return _func(*args, **kwargs)

        return cast(TVar, decorated)

    return wrapped


def cache_idempotent(*, ttl: int) -> Callable[[TVar], TVar]:

    def decorator(func: TVar) -> TVar:

        _func = cast(Callable[..., Any], func)

        @apm.trace(overridden_function=cache_idempotent)
        @functools.wraps(_func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            signature = inspect.signature(_func).bind(*args, **kwargs)

            cache_key_from_args = ''.join(
                f'{arg}_{value}' for arg, value in signature.arguments.items()
            )
            cache_key_from_func = \
                f'{_func.__module__}.{_func.__qualname__}'
            cache_key = f'{cache_key_from_func}:{cache_key_from_args}'

            try:
                ret = await aio.ensure_io_bound(cache.get, cache_key)

                if ret is None:
                    ret = await _func(*args, **kwargs)

                    await aio.ensure_io_bound(
                        cache.set, cache_key, ret, timeout=ttl,
                    )
                return ret
            except RedisClusterException as ex:
                LOGGER.exception(ex)
                return await _func(*args, **kwargs)

        return cast(TVar, wrapper)

    return decorator


def turn_args_into_kwargs(func: TVar) -> TVar:
    """Turn function's positional-arguments into keyword-arguments.

    Very useful when you want to keep an strongly typed signature in your
    function while using another decorators from this module that work on
    keyword arguments only for backwards compatibility reasons.

    This avoids functions with a typeless **parameters, and then 50 lines
    unpacking the arguments and casting them to the expected types.
    """

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def newfunc(*args: Any, **kwargs: Any) -> Any:
        # The first two arguments are django's self, and info references
        #   They can be safely left intact

        args_as_kwargs = dict(zip(
            inspect.getfullargspec(_func).args[2:], args[2:]
        ))

        return await _func(*args[0:2], **args_as_kwargs, **kwargs)

    return cast(TVar, newfunc)


def shield(func: TVar) -> TVar:
    """Catches and reports general Exceptions raised in decorated function"""

    _func = cast(Callable[..., Any], func)

    async def report(exception: Exception) -> None:
        LOGGER.error(
            'Shielded function raised a generic Exception',
            extra={
                'extra': {
                    'exception': exception,
                    'function': _func.__name__,
                }
            })

    if asyncio.iscoroutinefunction(_func):
        @functools.wraps(_func)
        async def shieldedfunc(*args: Any, **kwargs: Any) -> Any:
            try:
                return await _func(*args, **kwargs)
            except Exception as exception:  # pylint: disable=broad-except
                report(exception)

    else:
        @functools.wraps(_func)
        def shieldedfunc(*args: Any, **kwargs: Any) -> Any:
            try:
                return _func(*args, **kwargs)
            except Exception as exception:  # pylint: disable=broad-except
                async_to_sync(report)(exception)

    return cast(TVar, shieldedfunc)
