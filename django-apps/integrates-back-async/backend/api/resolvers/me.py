import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Set, Any, cast, Union

from ariadne import (
    convert_kwargs_to_snake_case,
    convert_camel_case_to_snake
)
from asgiref.sync import sync_to_async
from django.conf import settings
from jose import jwt
from mixpanel import Mixpanel
from social_core.exceptions import AuthException
from social_django.utils import load_strategy
from social_django.utils import load_backend
from graphql.type.definition import GraphQLResolveInfo

from backend.api.resolvers import (
    organization as organization_resolver,
    project as project_resolver,
)
from backend.dal.organization import (
    get_ids_for_user as get_user_organizations,
)
from backend.decorators import require_login
from backend.domain import (
    organization as org_domain,
    subscriptions as subscriptions_domain,
    tag as tag_domain,
    user as user_domain,
)
from backend.exceptions import InvalidExpirationTime
from backend.typing import (
    Me as MeType,
    Organization as OrganizationType,
    Project as ProjectType,
    SignInPayload as SignInPayloadType,
    SimplePayload as SimplePayloadType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils import aio
from backend import util
from backend import authz


# Constants
LOGGER = logging.getLogger(__name__)


async def _get_role(
        _: GraphQLResolveInfo,
        user_email: str,
        entity: str = 'USER',
        identifier: str = '',
        project_name: str = '') -> str:
    """Get role."""
    if project_name or (entity == 'PROJECT' and identifier):
        group_name = project_name or identifier
        role = await sync_to_async(authz.get_group_level_role)(
            user_email, group_name
        )
    elif entity == 'ORGANIZATION' and identifier:
        organization_id = identifier
        role = await sync_to_async(authz.get_organization_level_role)(
            user_email, organization_id
        )
    else:
        role = await sync_to_async(authz.get_user_level_role)(user_email)
    return cast(str, role)


async def _get_organizations(
        info: GraphQLResolveInfo,
        user_email: str) -> List[OrganizationType]:
    organization_ids = await get_user_organizations(user_email)
    organizations = await aio.materialize(
        organization_resolver.resolve(
            info, organization_id, as_field=True
        )
        for organization_id in organization_ids
    )
    return cast(List[OrganizationType], organizations)


async def _get_projects(
        info: GraphQLResolveInfo,
        user_email: str) -> List[ProjectType]:
    """Get projects."""
    project_names = await user_domain.get_projects(user_email)
    projects = await asyncio.gather(*[
        asyncio.create_task(
            project_resolver.resolve(info, project_name, as_field=True)
        )
        for project_name in project_names
    ])
    return projects


async def _get_access_token(_: GraphQLResolveInfo, user_email: str) -> str:
    """Get access token."""
    access_token = await user_domain.get_data(
        user_email, 'access_token')
    access_token_dict = {
        'hasAccessToken': bool(access_token),
        'issuedAt': str(access_token.get('iat', ''))
        if isinstance(access_token, dict)
        else ''
    }
    return json.dumps(access_token_dict)


async def _get_remember(_: GraphQLResolveInfo, user_email: str) -> bool:
    """Get remember preference."""
    remember = await user_domain.get_data(
        user_email, 'legal_remember'
    )
    return bool(remember)


async def _get_subscriptions_to_entity_report(
    _: GraphQLResolveInfo,
    user_email: str,
) -> List[Dict[str, str]]:
    return await subscriptions_domain.get_user_subscriptions_to_entity_report(
        user_email=user_email,
    )


async def _get_permissions(
        _: GraphQLResolveInfo,
        user_email: str,
        entity: str = 'USER',
        identifier: str = '',
        project_name: str = '') -> Set[str]:
    """Get the actions the user is allowed to perform."""
    if project_name or (entity == 'PROJECT' and identifier):
        group_name = project_name or identifier
        permissions = await authz.get_group_level_actions(
            user_email, group_name
        )
    elif entity == 'ORGANIZATION' and identifier:
        organization_id = identifier
        permissions = await authz.get_organization_level_actions(
            user_email, organization_id
        )
    else:
        permissions = await authz.get_user_level_actions(user_email)

    return permissions


async def _get_tags(
    _: GraphQLResolveInfo,
    user_email: str,
    organization_id: str
) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
    """Get tags."""
    org_name = await org_domain.get_name_by_id(organization_id)
    org_tags = await tag_domain.get_tags(org_name, ['projects', 'tag'])
    user_groups = await user_domain.get_projects(
        user_email, organization_id=organization_id
    )
    tag_info: List[Dict[str, Union[str, List[Dict[str, str]]]]] = [
        {
            'name': str(tag['tag']),
            'projects': [
                {'name': str(group)}
                for group in cast(List[str], tag['projects'])
            ]
        }
        for tag in org_tags
        if all([
            group in user_groups
            for group in cast(List[str], tag['projects'])
        ])
    ]
    return tag_info


async def _get_caller_origin(
        info: GraphQLResolveInfo,
        **_: Dict[Any, Any]) -> str:
    """Get caller_origin."""
    if hasattr(info.context, 'caller_origin'):
        origin = info.context.caller_origin
    else:
        origin = 'API'
    return cast(str, origin)


async def _resolve_fields(info: GraphQLResolveInfo) -> MeType:
    """Async resolve fields."""
    result: MeType = dict()

    for requested_field in info.field_nodes[0].selection_set.selections:
        if util.is_skippable(info, requested_field):
            continue
        jwt_content = util.get_jwt_content(info.context)
        params = {
            'user_email': jwt_content.get('user_email')
        }
        field_params = util.get_field_parameters(
            requested_field, info.variable_values
        )
        if field_params:
            params.update(field_params)
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_me(
        _: Any,
        info: GraphQLResolveInfo,
        caller_origin: str = '') -> MeType:
    """Resolve Me query."""
    jwt_content = util.get_jwt_content(info.context)
    user_email = jwt_content.get('user_email')

    info.context.caller_origin = origin = caller_origin or 'API'

    util.cloudwatch_log(
        info.context,
        f'Security: User {user_email} is accessing '
        f'Integrates using {origin}'  # pragma: no cover
    )
    return await _resolve_fields(info)


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_me_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Dict[str, str]) -> Any:
    """Wrap me mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


async def _do_subscribe_to_entity_report(
    _: Any,
    info: GraphQLResolveInfo,
    frequency: str,
    report_entity: str,
    report_subject: str,
) -> SimplePayloadType:
    success: bool = False
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']

    if await subscriptions_domain.can_subscribe_user_to_entity_report(
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    ):
        success = await subscriptions_domain.subscribe_user_to_entity_report(
            event_frequency=frequency,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )

        if success:
            util.cloudwatch_log(
                info.context,
                f'user: {user_email} edited subscription to '
                f'entity_report: {report_entity}/{report_subject} '
                f'frequency: {frequency}',
            )
        else:
            LOGGER.error(
                'Couldn\'t subscribe to %s report',
                report_entity,
                extra={'extra': locals()})
    else:
        util.cloudwatch_log(
            info.context,
            f'user: {user_email} attempted to edit subscription to '
            f'entity_report: {report_entity}/{report_subject} '
            f'frequency: {frequency} '
            f'without permission',
        )

    return SimplePayloadType(success=success)


async def _do_sign_in(
        _: Any,
        info: GraphQLResolveInfo,
        auth_token: str,
        provider: str) -> SignInPayloadType:
    """ Sign in with an OAuth2 access token """
    session_jwt = ''
    success = False

    try:
        strategy = load_strategy(info.context)
        auth_backend = load_backend(
            strategy=strategy, name=provider, redirect_uri=None)
        user = await sync_to_async(auth_backend.do_auth)(auth_token)
        email = user.email.lower()
        session_jwt = jwt.encode(
            {
                'user_email': email,
                'first_name': getattr(user, 'first_name'),
                'last_name': getattr(user, 'last_name'),
                'exp': datetime.utcnow() +
                timedelta(seconds=settings.MOBILE_SESSION_AGE),
                'sub': 'session_token',
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
        await sync_to_async(mp_obj.track)(
            email,
            'MobileAuth',
            {
                'email': email,
                'provider': provider
            }
        )
        success = True
    except AuthException as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return SignInPayloadType(
        session_jwt=session_jwt,
        success=success
    )


@require_login
async def _do_update_access_token(
        _: Any,
        info: GraphQLResolveInfo,
        expiration_time: int) -> UpdateAccessTokenPayloadType:
    """Resolve update_access_token mutation."""
    user_info = util.get_jwt_content(info.context)
    email = user_info['user_email']
    token_data = util.calculate_hash_token()
    session_jwt = ''
    success = False

    if util.is_valid_expiration_time(expiration_time):
        session_jwt = jwt.encode(
            {
                'user_email': email,
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name'],
                'jti': token_data['jti'],
                'iat': datetime.utcnow().timestamp(),
                'exp': expiration_time,
                'sub': 'api_token',
            },
            algorithm='HS512',
            key=settings.JWT_SECRET_API
        )

        success = await user_domain.update_access_token(
            email, token_data
        )
        if success:
            util.cloudwatch_log(
                info.context,
                (f'{user_info["user_email"]} '  # pragma: no cover
                 'update access token')
            )
        else:
            util.cloudwatch_log(
                info.context,
                (f'{user_info["user_email"]} '  # pragma: no cover
                 'attempted to update access token')
            )
    else:
        util.cloudwatch_log(
            info.context,
            (f'{user_info["user_email"]} '  # pragma: no cover
             'attempted to use expiration time '
             'greater than six months or minor '
             'than current time')
        )
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(
        success=success,
        session_jwt=session_jwt
    )


@require_login
async def _do_invalidate_access_token(
        _: Any,
        info: GraphQLResolveInfo) -> SimplePayloadType:
    """Resolve invalidate_access_token mutation."""
    user_info = util.get_jwt_content(info.context)

    success = await user_domain.remove_access_token(
        user_info['user_email']
    )
    if success:
        util.cloudwatch_log(
            info.context,
            (f'{user_info["user_email"]} '  # pragma: no cover
             'invalidate access token')
        )
    else:
        util.cloudwatch_log(
            info.context,
            (f'{user_info["user_email"]} '  # pragma: no cover
             'attempted to invalidate access token')
        )
    return SimplePayloadType(success=success)


async def _do_accept_legal(
        _: Any,
        info: GraphQLResolveInfo,
        remember: bool = False) -> SimplePayloadType:
    """Resolve accept_legal mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']

    success = await user_domain.update_legal_remember(
        user_email, remember
    )

    return SimplePayloadType(success=success)
