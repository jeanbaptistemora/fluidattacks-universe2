from aioextensions import (
    collect,
)
from app.utils import (
    get_redirect_url,
)
from authlib.integrations.base_client.errors import (
    MismatchingStateError,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    credentials as credentials_model,
)
from db_model.credentials.oauth import (
    OAUTH as ROAUTH,
)
from db_model.credentials.oauth.gitlab import (
    get_refresh_token,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
from httpx import (
    ConnectTimeout,
)
import logging
import logging.config
from newutils.datetime import (
    get_utc_now,
)
from organizations.domain import (
    has_access,
)
from organizations.validations import (
    validate_credentials_name_in_organization,
    validate_credentials_oauth,
)
from sessions.domain import (
    get_jwt_content,
)
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    RedirectResponse,
    Response,
)
from typing import (
    Optional,
)
from urllib.parse import (
    urlencode,
)
import uuid

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def do_gitlab_oauth(request: Request) -> Response:
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    if not await has_access(
        loaders=get_new_context(),
        email=email,
        organization_id=organization_id,
    ):
        raise PermissionError("Access denied")

    redirect_uri = get_redirect_url(request, "oauth_gitlab")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}"
    gitlab = ROAUTH.create_client("gitlab")

    return await gitlab.authorize_redirect(request, url)


async def oauth_gitlab(request: Request) -> RedirectResponse:
    try:
        user_info = await get_jwt_content(request)
        email: str = user_info["user_email"]
        organization_id: str = request.query_params["subject"]
        code: str = request.query_params["code"]
        if not await has_access(
            loaders=get_new_context(),
            email=email,
            organization_id=organization_id,
        ):
            raise PermissionError("Access denied")
        redirect = get_redirect_url(request, "oauth_gitlab")
        token: Optional[str] = await get_refresh_token(
            code=code, subject=organization_id, redirect_uri=redirect
        )
        if not token:
            raise OAuthError()
    except (ConnectTimeout, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    loaders: Dataloaders = get_new_context()
    name = f'Gitlab OAUTH {str(uuid.uuid4()).split("-", maxsplit=1)[0]}'
    credential = Credentials(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=OauthGitlabSecret(
                refresh_token=token,
            ),
            type=CredentialType.OAUTH,
            is_pat=False,
            azure_organization=None,
        ),
    )

    await collect(
        (
            validate_credentials_name_in_organization(
                loaders, credential.organization_id, credential.state.name
            ),
            validate_credentials_oauth(
                loaders, credential.organization_id, credential.owner
            ),
        )
    )
    await credentials_model.add(credential=credential)
    response = RedirectResponse(url="/home")

    return response
