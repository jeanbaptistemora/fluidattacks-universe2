import logging
import json
import sys
from typing import Any, Dict, Optional
import aiohttp

from aioextensions import (
    in_thread,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from mixpanel import Mixpanel

from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import require_login
from backend.domain import (
    subscriptions as subscriptions_domain,
    user as user_domain,
)
from backend.exceptions import InvalidExpirationTime
from backend.typing import (
    SignInPayload as SignInPayloadType,
    SimplePayload as SimplePayloadType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils import (
    datetime as datetime_utils,
)
from backend import util
from backend.utils import token as token_helper
from backend_new import settings
from backend_new.app import utils
from backend_new.settings.auth import (
    azure,
    BITBUCKET_ARGS,
    GOOGLE_ARGS
)

from backend_new.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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


async def get_provider_user_info(
    provider: str,
    token: str
) -> Optional[Dict[str, str]]:
    if provider == 'bitbucket':
        userinfo_endpoint = BITBUCKET_ARGS['userinfo_endpoint']
    elif provider == 'google':
        userinfo_endpoint = (
            f'{GOOGLE_ARGS["userinfo_endpoint"]}?access_token={token}'
        )
    elif provider == 'microsoft':
        userinfo_endpoint = azure.API_USERINFO_BASE_URL

    async with aiohttp.ClientSession() as session:
        async with session.get(
            userinfo_endpoint,
            headers={
                'Authorization': f'Bearer {token}'
            }
        ) as user:
            if user.status != 200:
                return None
            user = await user.read()
            user = json.loads(user)
            if 'given_name' not in user:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f'{userinfo_endpoint}/emails',
                        headers={
                            'Authorization': f'Bearer {token}'
                        }
                    ) as emails:
                        emails = await emails.json()
                        email = next(iter([
                            email.get('email', '')
                            for email in emails.get('values', '')
                            if email.get('is_primary')
                        ]), '')

                user['email'] = email
                user_name = user.get('display_name', '')
                user['given_name'] = user_name.split(' ')[0]
                user['family_name'] = \
                    user_name.split(' ')[1] if len(user_name) == 2 else ''
            return user


async def _do_sign_in(
        _: Any,
        _info: GraphQLResolveInfo,
        auth_token: str,
        provider: str) -> SignInPayloadType:
    """ Sign in with an OAuth2 access token """
    session_jwt = ''
    success = False

    user = await get_provider_user_info(provider, auth_token)
    if user:
        await utils.create_user(user)
        email = user['email'].lower()
        session_jwt = token_helper.new_encoded_jwt(
            {
                'user_email': email,
                'first_name': user.get('given_name'),
                'last_name': user.get('family_name'),
                'exp': datetime_utils.get_now_plus_delta(
                    seconds=settings.MOBILE_SESSION_AGE
                ),
                'sub': 'session_token',
            }
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
    else:
        LOGGER.exception('Mobile login failed', extra={'extra': locals()})

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
