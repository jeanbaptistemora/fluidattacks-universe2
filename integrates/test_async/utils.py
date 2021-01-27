import requests
import uuid

from datetime import datetime, timedelta

from starlette.responses import Response

from backend import util
from backend.api import apply_context_attrs
from backend.dal import (
    session as session_dal,
)
from backend.utils import token as token_helper
from back import settings


def create_dummy_simple_session(
    username: str = 'unittest',
    client: str = 'web',
) -> Response:
    request = requests.Request('GET', '/')
    request = apply_context_attrs(request)
    setattr(request, 'session', dict(
        username=username,
        session_key=str(uuid.uuid4())
    ))
    setattr(request, 'cookies', dict())

    return request


async def create_dummy_session(
    username: str = 'unittest',
    session_jwt=None
) -> Response:
    request = create_dummy_simple_session(username)
    payload = {
        'user_email': username,
        'first_name': 'unit',
        'last_name': 'test',
        'exp': datetime.utcnow() +
        timedelta(seconds=settings.SESSION_COOKIE_AGE),
        'sub': 'django_session',
        'jti': util.calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    if session_jwt:
        request.headers['Authorization'] = f'Bearer {session_jwt}'
    else:
        request.cookies[settings.JWT_COOKIE_NAME] = token
        await session_dal.add_element(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)

    return request
