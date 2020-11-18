# Starlette views file

# Standard library
import os
from typing import Dict
import aiohttp

# Third party libraries
from asgiref.sync import async_to_sync

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.starlette_client import OAuth
from authlib.common.security import generate_token

# Local libraries
from backend.api import IntegratesAPI
from backend.decorators import authenticate_session
from backend.domain import organization as org_domain
from backend.api.schema import SCHEMA

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


def unauthorized(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name='unauthorized.html',
        context={
            'request': request,
            'debug': settings.DEBUG,
        }
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


def get_azure_client(request: Request) -> OAuth:
    redirect_uri = utils.get_redirect_url(request, 'authz_azure')
    azure = AsyncOAuth2Client(
        settings.AZURE_ARGS['client_id'],
        settings.AZURE_ARGS['client_secret'],
        scope='https://graph.microsoft.com/.default openid email profile',
        redirect_uri=redirect_uri
    )
    return azure


async def handle_user(request: Request, user: Dict[str, str]) -> Request:
    request.session['username'] = user['email']
    request.session['first_name'] = user.get('given_name', '')
    request.session['last_name'] = user.get('family_name', '')
    await utils.create_user(request.session)

    return request


async def do_google_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, 'authz_google')
    google = OAUTH.create_client('google')
    return await google.authorize_redirect(request, redirect_uri)


async def do_azure_login(request: Request) -> Response:
    azure = get_azure_client(request)
    uri, _ = azure.create_authorization_url(
        settings.AZURE_ARGS['authorize_url'],
        nonce=generate_token()
    )
    return RedirectResponse(url=uri)


async def do_bitbucket_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, 'authz_bitbucket')
    bitbucket = OAUTH.create_client('bitbucket')
    return await bitbucket.authorize_redirect(request, redirect_uri)


async def authz(request: Request, client: OAuth) -> RedirectResponse:
    token = await client.authorize_access_token(request)

    if 'id_token' in token:
        user = await utils.get_jwt_userinfo(client, request, token)
    else:
        user = await utils.get_bitbucket_oauth_userinfo(client, token)

    request = await handle_user(request, user)

    return RedirectResponse(url='/new/home')


@authenticate_session  # type: ignore
@async_to_sync  # type: ignore
async def app(*request_args: Request) -> HTMLResponse:
    """ View for authenticated users"""
    request = utils.get_starlette_request(request_args)
    email = request.session.get('username')

    if email:
        if not await org_domain.get_user_organizations(email):
            response = unauthorized(request)
        else:
            context = {
                'request': request,
                'debug': settings.DEBUG,
                'js': f'{settings.STATIC_URL}/dashboard/app-bundle.min.js',
                'css': f'{settings.STATIC_URL}/dashboard/app-style.min.css',
                'delighted': f'{settings.STATIC_URL}/app/delighted.js'
            }
            response = TEMPLATING_ENGINE.TemplateResponse(
                name='app.html',
                context=context
            )

            jwt_token = utils.create_session_token(request.session)
            utils.set_token_in_response(response, jwt_token)
    else:
        response = unauthorized(request)
        response.delete_cookie(key=settings.JWT_COOKIE_NAME)

    return response


async def authz_google(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.google)


async def authz_azure(request: Request) -> HTMLResponse:
    azure = azure = get_azure_client(request)
    token = await azure.fetch_token(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        authorization_response=str(request.url)
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://graph.microsoft.com/oidc/userinfo',
            headers={
                'Authorization': f'Bearer {token["access_token"]}',
                'Host': 'graph.microsoft.com'
            }
        ) as user:
            request = await handle_user(request, await user.json())

    return RedirectResponse(url='/new/home')


async def authz_bitbucket(request: Request) -> HTMLResponse:
    return await authz(request, OAUTH.bitbucket)


APP = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/error401', error401),
        Route('/error500', error500),
        Route('/invalid_invitation', invalid_invitation),
        Route('/new/', login),
        Route('/new/authz_google', authz_google),
        Route('/new/authz_azure', authz_azure),
        Route('/new/authz_bitbucket', authz_bitbucket),
        Route('/new/dglogin', do_google_login),
        Route('/new/dalogin', do_azure_login),
        Route('/new/dblogin', do_bitbucket_login),
        Route('/new/api', IntegratesAPI(SCHEMA, debug=settings.DEBUG)),
        Route('/new/{full_path:path}', app),
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
