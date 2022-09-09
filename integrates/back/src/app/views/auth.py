# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Starlette authz-related views/functions

from api.mutations.sign_in import (
    log_stakeholder_in,
)
from app import (
    utils,
)
from authlib.integrations.base_client.errors import (
    MismatchingStateError,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from dataloaders import (
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
from httpx import (
    ConnectTimeout,
)
import logging
import logging.config
from newutils import (
    templates as templates_utils,
)
from sessions import (
    dal as sessions_dal,
)
from settings.auth import (
    OAUTH,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
    Response,
)
from typing import (
    Dict,
)
import uuid

LOGGER = logging.getLogger(__name__)


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_azure(request: Request) -> HTMLResponse:
    client = OAUTH.azure
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    email = user.get("email", user.get("upn", "")).lower()
    response = RedirectResponse(url="/home")
    await handle_user(
        request, response, {**user, "email": email, "given_name": user["name"]}
    )
    return response


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_bitbucket(request: Request) -> HTMLResponse:
    client = OAUTH.bitbucket
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_bitbucket_oauth_userinfo(client, token)
    response = RedirectResponse(url="/home")
    await handle_user(request, response, user)
    return response


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_google(request: Request) -> HTMLResponse:
    client = OAUTH.google
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    response = RedirectResponse(url="/home")
    await handle_user(request, response, user)
    return response


async def do_azure_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_azure")
    azure = OAUTH.create_client("azure")
    return await azure.authorize_redirect(request, redirect_uri)


async def do_bitbucket_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_bitbucket")
    bitbucket = OAUTH.create_client("bitbucket")
    return await bitbucket.authorize_redirect(request, redirect_uri)


@retry_on_exceptions(
    exceptions=(ConnectTimeout,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def do_google_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_google")
    google = OAUTH.create_client("google")
    return await google.authorize_redirect(request, redirect_uri)


async def handle_user(
    request: Request, response: HTMLResponse, user: Dict[str, str]
) -> None:
    email = user["email"]
    session_key = str(uuid.uuid4())
    request.session["session_key"] = session_key
    jwt_token = await utils.create_session_token(user)
    utils.set_token_in_response(response, jwt_token)
    await sessions_dal.create_session_web(request, email)
    await log_stakeholder_in(get_new_context(), user)
