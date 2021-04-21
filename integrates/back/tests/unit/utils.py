import requests
import uuid
from datetime import datetime, timedelta

from starlette.responses import Response

from back import settings
from backend import util
from backend.api import apply_context_attrs
from backend.dal.helpers.redis import redis_set_entity_attr
from newutils import token as token_helper


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
        'sub': 'starlette_session',
        'jti': util.calculate_hash_token()['jti'],
    }
    token = token_helper.new_encoded_jwt(payload)
    if session_jwt:
        request.headers['Authorization'] = f'Bearer {session_jwt}'
    else:
        request.cookies[settings.JWT_COOKIE_NAME] = token
        await redis_set_entity_attr(
            entity='session',
            attr='jti',
            email=payload['user_email'],
            value=payload['jti'],
            ttl=settings.SESSION_COOKIE_AGE
        )
        await redis_set_entity_attr(
            entity='session',
            attr='jwt',
            email=payload['user_email'],
            value=token,
            ttl=settings.SESSION_COOKIE_AGE
        )

    return request
