# -*- coding: utf-8 -*-
""" Decorators for FluidIntegrates. """

# Standard library
from datetime import datetime
import functools
import inspect
import logging
from typing import Any, Callable, Dict, cast, TypeVar

# Third party libraries
from aioextensions import (
    collect,
    in_thread,
    schedule,
)
from django.core.cache import cache
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from graphql import GraphQLError
from graphql.type import GraphQLResolveInfo
from rediscluster.nodemanager import RedisClusterException

# Local libraries
from backend.domain import (
    finding as finding_domain,
    organization as org_domain,
    vulnerability as vuln_domain
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
    function,
)

from backend_new import settings

from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TVar = TypeVar('TVar')
TFun = TypeVar('TFun', bound=Callable[..., Any])

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

    # Unique ID for this decorator function
    context_store_key: str = function.get_id(require_login)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        # The underlying request object being served
        context = args[1].context if len(args) > 1 else args[0]

        # Within the context of one request we only need to check this once
        # Future calls to this decorator will be passed trough
        if context.store[context_store_key]:
            return await _func(*args, **kwargs)

        try:
            user_data: Any = await util.get_jwt_content(context)
            if util.is_api_token(user_data):
                await verify_jti(
                    user_data['user_email'],
                    context.META.get('HTTP_AUTHORIZATION'),
                    user_data['jti']
                )
        except InvalidAuthorization:
            raise GraphQLError('Login required')
        else:
            context.store[context_store_key] = True
            return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


async def _resolve_from_event_id(context: Any, identifier: str) -> str:
    data = await context.loaders['event'].load(identifier)
    project_name: str = data['project_name']
    return project_name


async def _resolve_from_finding_id(context: Any, identifier: str) -> str:
    data = await context.loaders['finding'].load(identifier)
    project_name: str = data['project_name']
    return project_name


async def _resolve_from_vuln_id(context: Any, identifier: str) -> str:
    data = await context.loaders['single_vulnerability'].load(identifier)
    return await _resolve_from_finding_id(context, data.finding_id)


async def resolve_group_name(  # noqa: MC0001
    context: Any,
    args: Any,
    kwargs: Any,
) -> str:
    """Get project name based on args passed."""
    if args and hasattr(args[0], 'name'):
        name = args[0].name
    elif args and hasattr(args[0], 'project_name'):
        name = args[0].project_name
    elif args and hasattr(args[0], 'finding_id'):
        name = await _resolve_from_finding_id(context, args[0].finding_id)
    elif args and args[0] and 'name' in args[0]:
        name = args[0]['name']
    elif args and args[0] and 'project_name' in args[0]:
        name = args[0]['project_name']
    elif 'project_name' in kwargs:
        name = kwargs['project_name']
    elif 'group_name' in kwargs:
        name = kwargs['group_name']
    elif 'finding_id' in kwargs:
        name = await _resolve_from_finding_id(context, kwargs['finding_id'])
    elif 'draft_id' in kwargs:
        name = await _resolve_from_finding_id(context, kwargs['draft_id'])
    elif 'event_id' in kwargs:
        name = await _resolve_from_event_id(context, kwargs['event_id'])
    elif 'vuln_uuid' in kwargs:
        name = await _resolve_from_vuln_id(context, kwargs['vuln_uuid'])
    elif settings.DEBUG:
        raise Exception('Unable to identify project')
    else:
        name = ''

    if isinstance(name, str):
        name = name.lower()

    return cast(str, name)


def enforce_group_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the group-level role."""

    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], 'context'):
            context = args[0].context
        elif hasattr(args[1], 'context'):
            context = args[1].context
        else:
            GraphQLError('Could not get context from request.')

        user_data = await util.get_jwt_content(context)
        subject = user_data['user_email']
        object_ = await resolve_group_name(context, args, kwargs)
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

        enforcer = await authz.get_group_level_enforcer(subject, context.store)

        if not enforcer(object_, action):
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
            kwargs.get('organization_name') or
            args[0]['id']
        )
        organization_id = (
            organization_identifier
            if organization_identifier.startswith('ORG#')
            else await org_domain.get_id_by_name(organization_identifier)
        )
        user_data = await util.get_jwt_content(context)

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

        enforcer = await authz.get_organization_level_enforcer(subject)

        if not enforcer(object_, action):
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

        user_data = await util.get_jwt_content(context)

        subject = user_data['user_email']
        object_ = 'self'
        action = f'{_func.__module__}.{_func.__qualname__}'.replace('.', '_')

        enforcer = await authz.get_user_level_enforcer(subject)

        if not enforcer(object_, action):
            util.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError('Access denied')
        return await _func(*args, **kwargs)
    return cast(TVar, verify_and_call)


async def verify_jti(email: str, context: Dict[str, str], jti: str) -> None:
    if not await has_valid_access_token(email, context, jti):
        raise InvalidAuthorization()


def require_attribute(attribute: str) -> Callable[[TVar], TVar]:

    def wrapper(func: TVar) -> TVar:

        _func = cast(Callable[..., Any], func)

        @functools.wraps(_func)
        async def resolve_and_call(*args: Any, **kwargs: Any) -> Any:
            if hasattr(args[0], 'context'):
                context = args[0].context
            elif hasattr(args[1], 'context'):
                context = args[1].context
            else:
                GraphQLError('Could not get context from request.')

            group = await resolve_group_name(context, args, kwargs)

            # Unique ID for this decorator function
            context_store_key: str = function.get_id(
                require_attribute, attribute, group,
            )

            # Within the context of one request we only need to check this once
            # Future calls to this decorator will be passed trough
            if not context.store[context_store_key]:
                enforcer = await authz.get_group_service_attributes_enforcer(
                    group,
                )

                if not enforcer(attribute):
                    raise GraphQLError('Access denied')

            context.store[context_store_key] = True
            return await _func(*args, **kwargs)

        return cast(TVar, resolve_and_call)

    return wrapper


# Factory functions
REQUIRE_INTEGRATES = require_attribute('has_integrates')
REQUIRE_FORCES = require_attribute('has_forces')
REQUIRE_DRILLS_WHITE = require_attribute('has_drills_white')


def require_integrates(func: TVar) -> TVar:
    return REQUIRE_INTEGRATES(func)


def require_forces(func: TVar) -> TVar:
    return REQUIRE_FORCES(func)


def require_drills_white(func: TVar) -> TVar:
    return REQUIRE_DRILLS_WHITE(func)


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

        user_data = await util.get_jwt_content(context)
        user_email = user_data['user_email']

        organization_id = (
            organization_identifier
            if organization_identifier.startswith('ORG#')
            else await org_domain.get_id_by_name(organization_identifier)
        )

        role, has_access = await collect([
            authz.get_organization_level_role(user_email, organization_id),
            org_domain.has_user_access(organization_id, user_email)
        ])

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
        if not finding_id:
            vuln = await vuln_domain.get(kwargs['vuln_uuid'])
            finding_id = vuln['finding_id']

        finding = await context.loaders['finding'].load(finding_id)
        if finding_domain.is_deleted(finding):
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
            cache.set(key_name, ret, timeout=settings.CACHE_TTL)
            return ret
        except RedisClusterException as ex:
            LOGGER.exception(ex, extra=dict(extra=locals()))
            return _func(*args, **kwargs)
    return cast(TVar, decorated)


def get_entity_cache_async(func: TVar) -> TVar:
    """Get cached response of a GraphQL entity if it exists."""

    _func = cast(Callable[..., Any], func)

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
            ret = await in_thread(cache.get, key_name)

            if ret is None:
                ret = await _func(*args, **kwargs)

                await in_thread(
                    cache.set, key_name, ret, timeout=settings.CACHE_TTL,
                )
            return ret
        except RedisClusterException as ex:
            LOGGER.exception(ex, extra=dict(extra=locals()))
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
                ret = await in_thread(cache.get, cache_key)

                if ret is None:
                    ret = await _func(*args, **kwargs)

                    await in_thread(
                        cache.set, cache_key, ret, timeout=ttl,
                    )
                return ret
            except RedisClusterException as ex:
                LOGGER.exception(ex, extra=dict(extra=locals()))
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


def concurrent_decorators(
    *decorators: Callable[[Any], Any],
) -> Callable[[TFun], TFun]:
    """Decorator to fusion many decorators which will be executed concurrently.

    Either:
    - All decorators succeed and the decorated function is called,
    - Any decorator fail and the error is propagated to the caller.

    In the second case the propagated error is guaranteed to come from the
    first task to raise.
    """
    if len(decorators) <= 1:
        raise ValueError('Expected at least 2 decorators as arguments')

    def decorator(func: TFun) -> TFun:

        @functools.wraps(func)
        async def dummy(*_: Any, **__: Any) -> bool:
            """Dummy function to mimic `func`."""
            return True

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            success = []
            tasks = iter(list(map(schedule, [
                dec(dummy)(*args, **kwargs) for dec in decorators
            ])))

            try:
                for task in tasks:
                    task_result = await task
                    success.append(task_result.result())  # may rise
            finally:
                # If two or more decorators raised exceptions let's propagate
                # only the first to arrive and cancel the remaining ones
                # to avoid an ugly traceback, also because if one failed
                # there is no purpose in letting the remaining ones run
                for task in tasks:
                    task.cancel()

            # If everything succeed let's call the decorated function
            if success and all(success):
                return await func(*args, **kwargs)

            # May never happen as decorators raise something on errors
            # But it's nice to have a default value here
            raise RuntimeError('Decorators did not success')

        return cast(TFun, wrapper)

    return decorator
