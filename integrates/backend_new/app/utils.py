# Standard library
from datetime import datetime, timedelta
from typing import cast, Dict
from jose import jwt

# Third party libraries
from aioextensions import (
    collect,
    schedule
)
from starlette.requests import Request
from starlette.responses import HTMLResponse

from authlib.integrations.starlette_client import OAuth

# Local libraries
from backend.domain import user as user_domain
from backend import authz, mailer, util

from backend_new import settings

from __init__ import (
    FI_COMMUNITY_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS
)


def create_session_token(user: Dict[str, str]) -> str:
    jti = util.calculate_hash_token()['jti']
    jwt_token = jwt.encode(
        dict(
            user_email=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            exp=(
                datetime.utcnow() +
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            ),
            sub='starlette_session',
            jti=jti,
        ),
        algorithm='HS512',
        key=settings.JWT_SECRET,
    )

    return cast(str, jwt_token)


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


async def autoenroll_user(email: str) -> None:
    new_user_user_level_role: str = 'customer'
    new_user_group_level_role: str = 'customer'

    await user_domain.create_without_project(
        email=email,
        role=new_user_user_level_role
    )

    for group in FI_COMMUNITY_PROJECTS.split(','):
        await collect([
            user_domain.update_project_access(email, group, access=True),
            authz.grant_group_level_role(
                email,
                group,
                new_user_group_level_role
            )
        ])


async def create_user(user: Dict[str, str]) -> None:
    first_name = user['first_name'][:29]
    last_name = user['last_name'][:29]
    email = user['username'].lower()

    today = user_domain.get_current_date()
    data_dict = {
        'first_name': first_name,
        'last_login': today,
        'last_name': last_name,
        'date_joined': today
    }

    if not await user_domain.is_registered(email):
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
        await user_domain.update_multiple_user_attributes(
            email, data_dict
        )
    else:
        if await user_domain.get_data(email, 'first_name'):
            await user_domain.update_last_login(email)
        else:
            await user_domain.update_multiple_user_attributes(
                email, data_dict
            )
