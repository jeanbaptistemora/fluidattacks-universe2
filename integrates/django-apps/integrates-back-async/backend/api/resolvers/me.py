import asyncio
import json
import logging
import sys
from typing import Dict, List, Any, cast

from aioextensions import (
    in_thread,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from django.conf import settings
from jose import jwt
from mixpanel import Mixpanel
from social_core.exceptions import AuthException
from social_django.utils import load_strategy
from social_django.utils import load_backend
from graphql.type.definition import GraphQLResolveInfo

from backend.api.resolvers import (
    project as project_resolver,
)
from backend.decorators import require_login
from backend.domain import (
    subscriptions as subscriptions_domain,
    user as user_domain,
)
from backend.exceptions import InvalidExpirationTime
from backend.typing import (
    Project as ProjectType,
    SignInPayload as SignInPayloadType,
    SimplePayload as SimplePayloadType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils import (
    datetime as datetime_utils,
)
from backend import util
from backend import authz
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

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
        role = await authz.get_group_level_role(
            user_email, group_name
        )
    elif entity == 'ORGANIZATION' and identifier:
        organization_id = identifier
        role = await authz.get_organization_level_role(
            user_email, organization_id
        )
    else:
        role = await authz.get_user_level_role(user_email)
    return cast(str, role)


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
    user_info = await util.get_jwt_content(info.context)
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
        user = await in_thread(
            auth_backend.do_auth,
            auth_token,
            client='mobile'
        )
        email = user.email.lower()
        session_jwt = jwt.encode(
            {
                'user_email': email,
                'first_name': getattr(user, 'first_name'),
                'last_name': getattr(user, 'last_name'),
                'exp': datetime_utils.get_now_plus_delta(
                    seconds=settings.MOBILE_SESSION_AGE
                ),
                'sub': 'session_token',
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        mp_obj = Mixpanel(settings.MIXPANEL_API_TOKEN)
        await in_thread(
            mp_obj.track,
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
    user_info = await util.get_jwt_content(info.context)
    email = user_info['user_email']
    try:
        result = await user_domain.update_access_token(
            email,
            expiration_time,
            first_name=user_info['first_name'],
            last_name=user_info['last_name'])
        if result.success:
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
        return result
    except InvalidExpirationTime as exc:
        util.cloudwatch_log(
            info.context,
            (f'{user_info["user_email"]} '  # pragma: no cover
             'attempted to use expiration time '
             'greater than six months or minor '
             'than current time')
        )
        raise exc


@require_login
async def _do_invalidate_access_token(
        _: Any,
        info: GraphQLResolveInfo) -> SimplePayloadType:
    """Resolve invalidate_access_token mutation."""
    user_info = await util.get_jwt_content(info.context)

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
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']

    success = await user_domain.update_legal_remember(
        user_email, remember
    )

    return SimplePayloadType(success=success)


@require_login
async def _do_add_push_token(
    _: Any,
    info: GraphQLResolveInfo,
    token: str
) -> SimplePayloadType:
    """ Save push token """
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    success = await user_domain.add_push_token(user_email, token)

    return SimplePayloadType(success=success)
