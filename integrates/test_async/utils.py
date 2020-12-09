import requests
import uuid

from collections import defaultdict
from datetime import datetime, timedelta

from starlette.responses import Response

from jose import jwt
from backend import util
from backend.api import apply_context_attrs
from backend_new import settings


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
    token = jwt.encode(
        payload,
        algorithm='HS512',
        key=settings.JWT_SECRET,
    )
    if session_jwt:
        request.headers['Authorization'] = f'Bearer {session_jwt}'
    else: 
        request.cookies[settings.JWT_COOKIE_NAME] = token
        await util.save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)

    return request
