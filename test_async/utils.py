from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.response import HttpResponseBase
from django.test.client import RequestFactory
from jose import jwt
from backend import util


def create_dummy_simple_session(
    username: str = 'unittest'
) -> HttpResponseBase:
    request: HttpResponseBase = RequestFactory().get('/')
    middleware = SessionMiddleware()
    middleware.process_request(request)
    middleware.process_request(request)
    request.session['username'] = username
    request.session.save()
    return request


def create_dummy_session(
    username: str = 'unittest'
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
    request.COOKIES[settings.JWT_COOKIE_NAME] = token
    util.save_token(f'fi_jwt:{payload["jti"]}', token, settings.SESSION_COOKIE_AGE)
    return request
