# Starlette views file

# Standard library
import os
from typing import Any

# Third party libraries
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from authlib.integrations.starlette_client import OAuth

# Local libraries
from backend.api import IntegratesAPI

from backend_new.api.schema import SCHEMA
from backend_new.app.middleware import CustomRequestMiddleware
import backend_new.app.utils as utils
from backend_new import settings

from __init__ import (
    FI_STARLETTE_TEST_KEY
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluidintegrates.settings')

TEMPLATING_ENGINE = Jinja2Templates(directory=settings.TEMPLATES_DIR)

OAUTH = OAuth()
OAUTH.register(**settings.GOOGLE_ARGS)
OAUTH.register(**settings.AZURE_ARGS)
OAUTH.register(**settings.BITBUCKET_ARGS)


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


def invalid_invitation(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='invalid_invitation.html',
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


async def do_google_login(request: Request) -> Any:
    redirect_uri = request.url_for('authz_google').replace(' ', '')
    google = OAUTH.create_client('google')
    return await google.authorize_redirect(request, redirect_uri)


async def do_azure_login(request: Request) -> Any:
    redirect_uri = request.url_for('authz_azure').replace(' ', '')
    azure = OAUTH.create_client('azure')
    return await azure.authorize_redirect(request, redirect_uri)


async def do_bitbucket_login(request: Request) -> Any:
    redirect_uri = request.url_for('authz_bitbucket').replace(' ', '')
    bitbucket = OAUTH.create_client('bitbucket')
    return await bitbucket.authorize_redirect(request, redirect_uri)


async def authz(request: Request, client: OAuth) -> RedirectResponse:
    token = await client.authorize_access_token(request)

    if 'id_token' in token:
        user = await utils.get_jwt_userinfo(client, request, token)
    else:
        user = await utils.get_bitbucket_oauth_userinfo(client, token)

    request.session['username'] = user['email']
    request.session['first_name'] = user.get('given_name', '')
    request.session['last_name'] = user.get('family_name', '')

    return RedirectResponse(url='/new/home')


async def app(request: Request) -> HTMLResponse:
    """ View for authenticated users"""
    if 'username' in request.session:
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

        jwt_token = utils.create_session_token(request.session)
        utils.set_token_in_response(response, jwt_token)
    else:
        response = TEMPLATING_ENGINE.TemplateResponse(
            name='unauthorized.html',
            context={
                'request': request,
                'debug': settings.DEBUG,
            }
        )
        response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def authz_google(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.google)


async def authz_azure(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.azure)


async def authz_bitbucket(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.bitbucket)


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/new/', login),
        Route('/new/authz_google', authz_google),
        Route('/new/authz_azure', authz_azure),
        Route('/new/authz_bitbucket', authz_bitbucket),
        Route('/new/dglogin', do_google_login),
        Route('/new/dalogin', do_azure_login),
        Route('/new/dblogin', do_bitbucket_login),
        Route('/new/api/', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/error401', error401),
        Route('/error500', error500),
        Route('/new/app', app),
        Route('/new/{full_path:path}/', app),
        Route('/invalid_invitation', invalid_invitation),
        Mount(
            '/static',
            StaticFiles(directory=f'{settings.TEMPLATES_DIR}/static'),
            name='static'
        )
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=FI_STARLETTE_TEST_KEY),
        Middleware(CustomRequestMiddleware)
    ]
)
