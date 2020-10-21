# Standard library
from typing import Any

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
import backend_new.app.utils as utils

from __init__ import (
    FI_GOOGLE_OAUTH2_KEY,
    FI_GOOGLE_OAUTH2_SECRET,
    FI_STARLETTE_TEST_KEY
)

TEMPLATES_DIR = 'backend_new/app/templates'
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
    user = dict(await OAUTH.google.parse_id_token(request, token))
    request.session['username'] = user['email']
    request.session['first_name'] = user['given_name']
    request.session['last_name'] = user['family_name']
    response = TEMPLATING_ENGINE.TemplateResponse(
        name='app.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
            'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
            'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css',
            'delighted': f'{settings.STATIC_URL}/app/delighted.js'
        }
    )

    jwt_token = utils.create_session_token(user)
    utils.set_token_in_response(response, jwt_token)

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
