# Standard library
import logging
import json
from typing import (
    Any,
    cast,
    Dict,
    Optional
)

# Third party libraries
import aiohttp
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back import settings
from back.app import utils
from back.settings import LOGGING
from back.settings.auth import (
    azure,
    BITBUCKET_ARGS,
    GOOGLE_ARGS
)
from backend.typing import SignInPayload as SignInPayloadType
from newutils import (
    analytics,
    datetime as datetime_utils,
    token as token_helper,
)


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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

            return cast(Optional[Dict[str, str]], user)


@convert_kwargs_to_snake_case  # type: ignore
async def mutate(
    _: Any,
    _info: GraphQLResolveInfo,
    auth_token: str,
    provider: str
) -> SignInPayloadType:
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
        await analytics.mixpanel_track(
            email,
            'MobileAuth',
            provider=provider
        )
        success = True
    else:
        LOGGER.exception('Mobile login failed', extra={'extra': locals()})

    return SignInPayloadType(
        session_jwt=session_jwt,
        success=success
    )
