# Starlette authz-related views/functions

# Standard library
from typing import Dict
import aiohttp

# Third party libraries
from aioextensions import in_thread
import bugsnag

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.starlette_client import OAuth
from authlib.common.security import generate_token

# Local libraries
from backend import util
from backend.domain import user as user_domain

import backend_new.app.utils as utils
from backend_new.settings.auth import (
    azure,
    BITBUCKET_ARGS,
    GOOGLE_ARGS
)


OAUTH = OAuth()
OAUTH.register(**GOOGLE_ARGS)
OAUTH.register(**BITBUCKET_ARGS)


def get_azure_client(request: Request) -> OAuth:
    redirect_uri = utils.get_redirect_url(request, 'authz_azure')
    azure_client = AsyncOAuth2Client(
        azure.CLIENT_ID,
        azure.CLIENT_SECRET,
        scope=f'{azure.API_BASE_URL}.default {azure.SCOPE}',
        redirect_uri=redirect_uri
    )

    return azure_client


async def handle_user(request: Request, user: Dict[str, str]) -> Request:
    request.session['username'] = user['email'].lower()
    request.session['first_name'] = user.get('given_name', '')
    request.session['last_name'] = user.get('family_name', '')
    await utils.create_user(request.session)

    return request


async def do_google_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, 'authz_google')
    google = OAUTH.create_client('google')
    return await google.authorize_redirect(request, redirect_uri)


async def do_azure_login(request: Request) -> Response:
    azure_client = get_azure_client(request)
    uri, _ = azure_client.create_authorization_url(
        azure.AUTHZ_URL,
        nonce=generate_token()
    )

    return RedirectResponse(url=uri)


async def do_bitbucket_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, 'authz_bitbucket')
    bitbucket = OAUTH.create_client('bitbucket')
    return await bitbucket.authorize_redirect(request, redirect_uri)


async def authz_google(request: Request) -> HTMLResponse:
    client = OAUTH.google
    token = await client.authorize_access_token(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    request = await handle_user(request, user)

    return RedirectResponse(url='/new/home')


async def authz_azure(request: Request) -> HTMLResponse:
    azure_client = get_azure_client(request)
    token = await azure_client.fetch_token(
        azure.TOKEN_URL,
        authorization_response=str(request.url)
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(
            azure.API_USERINFO_BASE_URL,
            headers={
                'Authorization': f'Bearer {token["access_token"]}',
                'Host': 'graph.microsoft.com'
            }
        ) as user:
            request = await handle_user(request, await user.json())

    return RedirectResponse(url='/new/home')


async def authz_bitbucket(request: Request) -> HTMLResponse:
    client = OAUTH.bitbucket
    token = await client.authorize_access_token(request)
    user = await utils.get_bitbucket_oauth_userinfo(client, token)
    request = await handle_user(request, user)

    return RedirectResponse(url='/new/home')


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get('url_token')
    redir = '/new'
    token_exists = await util.token_exists(f'fi_urltoken:{url_token}')

    if token_exists:
        token_unused = await user_domain.complete_user_register(url_token)
        if not token_unused:
            redir = '/invalid_invitation'
    else:
        await in_thread(bugsnag.notify, Exception('Invalid token'), 'warning')
        redir = '/invalid_invitation'

    return RedirectResponse(url=redir)
