# Standard library
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Any,
    Dict,
)

# Third party libraries
from aioextensions import (
    collect,
    schedule,
)
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import HTMLResponse

# Local libraries
from back import settings
from backend import (
    authz,
    mailer,
    util,
)
from backend.dal.helpers.redis import redis_set_entity_attr
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from organizations import domain as orgs_domain
from newutils import (
    analytics,
    datetime as datetime_utils,
    token as token_helper,
)
from users import domain as users_domain
from __init__ import (
    FI_COMMUNITY_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
)


async def create_session_token(user: Dict[str, str]) -> str:
    jti = util.calculate_hash_token()['jti']
    user_email = user['username']
    jwt_token: str = token_helper.new_encoded_jwt(
        dict(
            user_email=user_email,
            first_name=user['first_name'],
            last_name=user['last_name'],
            exp=(
                datetime.utcnow() +
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            ),
            sub='starlette_session',
            jti=jti,
        )
    )

    await redis_set_entity_attr(
        entity='session',
        attr='jti',
        email=user_email,
        value=jti,
        ttl=settings.SESSION_COOKIE_AGE
    )
    await redis_set_entity_attr(
        entity='session',
        attr='jwt',
        email=user_email,
        value=jwt_token,
        ttl=settings.SESSION_COOKIE_AGE
    )

    return jwt_token


def set_token_in_response(response: HTMLResponse, token: str) -> HTMLResponse:
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        samesite=settings.JWT_COOKIE_SAMESITE,
        value=token,
        secure=True,
        httponly=True,
        max_age=settings.SESSION_COOKIE_AGE
    )

    return response


async def get_bitbucket_oauth_userinfo(
    client: OAuth,
    token: Dict[str, str]
) -> Dict[str, str]:
    query_headers = {'Authorization': f'Bearer {token["access_token"]}'}
    user = await client.get(
        'user',
        token=token,
        headers=query_headers
    )
    emails = await client.get(
        'user/emails',
        token=token,
        headers=query_headers
    )

    user_name = user.json().get('display_name', '')
    email = next(iter([
        email.get('email', '')
        for email in emails.json().get('values', '')
        if email.get('is_primary')
    ]), '')
    return {
        'email': email,
        'given_name': user_name.split(' ')[0],
        'family_name': user_name.split(' ')[1] if len(user_name) == 2 else '',
    }


async def get_jwt_userinfo(
    client: OAuth,
    request: Request,
    token: str
) -> Dict[str, str]:
    return dict(await client.parse_id_token(request, token))


def get_redirect_url(request: Request, pattern: str) -> Any:
    return request.url_for(pattern).replace('http:', 'https:')


async def autoenroll_user(email: str) -> None:
    new_user_user_level_role: str = 'customer'
    new_user_group_level_role: str = 'customer'

    await groups_domain.create_without_group(
        email=email,
        role=new_user_user_level_role
    )

    for group in FI_COMMUNITY_PROJECTS.split(','):
        await collect([
            group_access_domain.update_has_access(email, group, True),
            authz.grant_group_level_role(
                email,
                group,
                new_user_group_level_role
            )
        ])


async def create_user(user: Dict[str, str]) -> None:
    first_name = user.get('given_name', '')[:29]
    last_name = user.get('family_name', '')[:29]
    email = user['email'].lower()

    today = datetime_utils.get_now_as_str()
    data_dict = {
        'first_name': first_name,
        'last_login': today,
        'last_name': last_name,
        'date_joined': today
    }

    if not await users_domain.is_registered(email):
        await analytics.mixpanel_track(email, 'Register')
        if not await orgs_domain.get_user_organizations(email):
            await autoenroll_user(email)

        schedule(
            mailer.send_mail_new_user(
                email_to=[FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS],
                context={
                    'name_user': f'{first_name} {last_name}',
                    'mail_user': email,
                }
            )
        )
        await users_domain.update_multiple_user_attributes(
            email, data_dict
        )
    else:
        if await users_domain.get_data(email, 'first_name'):
            await users_domain.update_last_login(email)
        else:
            await users_domain.update_multiple_user_attributes(
                email, data_dict
            )
