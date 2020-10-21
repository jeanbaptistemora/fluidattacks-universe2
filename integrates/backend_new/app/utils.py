# Standard library
from datetime import datetime, timedelta
from typing import cast, Dict
from jose import jwt

# Third party libraries
from starlette.responses import HTMLResponse

# Local libraries
from backend import util

from backend_new import settings


def create_session_token(user: Dict[str, str]) -> str:
    jwt_token = jwt.encode(
        dict(
            user_email=user['email'],
            first_name=user['given_name'],
            last_name=user['family_name'],
            exp=(
                datetime.utcnow() +
                timedelta(seconds=settings.SESSION_COOKIE_AGE)
            ),
            sub='starlette_session',
            jti=util.calculate_hash_token()['jti'],
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
