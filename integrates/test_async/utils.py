from collections import defaultdict
from datetime import datetime, timedelta
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.response import HttpResponseBase
from django.test.client import RequestFactory
from jose import jwt
from backend import util
from backend.api import apply_context_attrs
from backend_new import settings


def create_dummy_simple_session(
    username: str = 'unittest',
    client: str = 'web',
) -> HttpResponseBase:
    request: HttpResponseBase = RequestFactory().get('/')
    request = apply_context_attrs(request)
    middleware = SessionMiddleware()
    middleware.process_request(request)
    middleware.process_request(request)
    request.session['client'] = client
    request.session['username'] = username
    request.session.save()
    return request


async def create_dummy_session(
    username: str = 'unittest',
    session_jwt=None
) -> HttpResponseBase:
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
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {session_jwt}'
    else: 
        request.COOKIES[settings.JWT_COOKIE_NAME] = token
        await util.save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
    return request
