# Standard library
import base64
import json
from typing import Any
from jose import jwt

# Third party libraries
from ariadne.asgi import GraphQL

from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from authlib.integrations.starlette_client import OAuth

# Local libraries
from backend.api.schema import SCHEMA

from backend_new import settings

from __init__ import (
    FI_GOOGLE_OAUTH2_KEY,
    FI_GOOGLE_OAUTH2_SECRET,
    FI_STARLETTE_TEST_KEY
)

TEMPLATES_DIR = 'backend_new/templates'
TEMPLATING_ENGINE = Jinja2Templates(directory=TEMPLATES_DIR)
OAUTH = OAuth()
OAUTH.register(
    name='google',
    client_id=FI_GOOGLE_OAUTH2_KEY,
    client_secret=FI_GOOGLE_OAUTH2_SECRET,
    server_metadata_url=settings.GOOGLE_CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def error500(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='HTTP500.html',
        context={'request': request}
    )


def error401(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='HTTP401.html',
        context={'request': request}
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='login.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
            'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
            'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css'
        }
    )


async def do_login(request: Request) -> Any:
    redirect_uri = request.url_for('authz').replace(' ', '')
    google = OAUTH.create_client('google')
    return await google.authorize_redirect(request, redirect_uri)


async def authz(request: Request) -> HTMLResponse:
    token = await OAUTH.google.authorize_access_token(request)
    user = await OAUTH.google.parse_id_token(request, token)
    request.session['username'] = dict(user)['email']
    response = TEMPLATING_ENGINE.TemplateResponse(
        name='app.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
            'username': request.session['username'],
            'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
            'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css',
            'delighted': f'{settings.STATIC_URL}/app/delighted.js'
        }
    )

    # convert SH256 google jwt to HS512 so we can handle it in our backend
    jwt_payload = token['id_token'].split('.')[1]
    payload = json.loads(
        base64.b64decode(
            jwt_payload + '=' * (-len(jwt_payload) % 4)
        ).decode('utf-8')
    )
    jwt_token = jwt.encode(
        payload,
        key=settings.JWT_SECRET,
        algorithm='HS512'
    )

    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        samesite=settings.JWT_COOKIE_SAMESITE,
        value=jwt_token,
        secure=True,
        httponly=True,
        max_age=settings.SESSION_COOKIE_AGE
    )
    return response


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/new/', login),
        Route('/new/login', authz),
        Route('/new/dlogin', do_login),
        Route('/new/api/', GraphQL(SCHEMA, debug=settings.DEBUG)),
        Route('/error401', error401),
        Route('/error500', error500),
        Mount(
            '/static',
            StaticFiles(directory=f'{TEMPLATES_DIR}/static'),
            name='static'
        )
    ],
)

# anyway, not used, just required
APP.add_middleware(SessionMiddleware, secret_key=FI_STARLETTE_TEST_KEY)
