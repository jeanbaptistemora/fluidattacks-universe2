# Starlette authz-related views/functions

from api.mutations.sign_in import (
    log_user_in,
)
from app import (
    utils,
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


async def authz_azure(request: Request) -> HTMLResponse:
    client = OAUTH.azure
    token = await client.authorize_access_token(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    email = user.get("email", user.get("upn", "")).lower()
    await handle_user(
        request, {**user, "email": email, "given_name": user["name"]}
    )
    return RedirectResponse(url="/home")


async def authz_bitbucket(request: Request) -> HTMLResponse:
    client = OAUTH.bitbucket
    token = await client.authorize_access_token(request)
    user = await utils.get_bitbucket_oauth_userinfo(client, token)
    await handle_user(request, user)
    return RedirectResponse(url="/home")


async def authz_google(request: Request) -> HTMLResponse:
    client = OAUTH.google
    token = await client.authorize_access_token(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    await handle_user(request, user)
    return RedirectResponse(url="/home")


async def do_azure_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_azure")
    azure = OAUTH.create_client("azure")
    return await azure.authorize_redirect(request, redirect_uri)


async def do_bitbucket_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_bitbucket")
    bitbucket = OAUTH.create_client("bitbucket")
    return await bitbucket.authorize_redirect(request, redirect_uri)


async def do_google_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_google")
    google = OAUTH.create_client("google")
    return await google.authorize_redirect(request, redirect_uri)


async def handle_user(request: Request, user: Dict[str, str]) -> Request:
    session_key = str(uuid.uuid4())

    request.session["username"] = user["email"]
    request.session["first_name"] = user.get("given_name", "")
    request.session["last_name"] = user.get("family_name", "")
    request.session["session_key"] = session_key

    await sessions_dal.create_session_web(request)
    await log_user_in(user)
