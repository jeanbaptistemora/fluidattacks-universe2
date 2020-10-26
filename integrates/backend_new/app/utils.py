# Standard library
from datetime import datetime, timedelta
from typing import cast, Dict
from jose import jwt

# Third party libraries
from starlette.requests import Request
from starlette.responses import HTMLResponse

from authlib.integrations.starlette_client import OAuth

# Local libraries
from backend import util

from backend_new import settings


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
