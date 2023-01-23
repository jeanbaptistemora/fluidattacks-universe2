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
from contextlib import (
    suppress,
)
from custom_exceptions import (
    CredentialAlreadyExists,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as credentials_model,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
from db_model.organizations.types import (
    Organization,
)
from httpx import (
    ConnectTimeout,
)
import logging
import logging.config
from newutils.datetime import (
    get_plus_delta,
    get_utc_now,
)
from oauth import (
    OAUTH as ROAUTH,
)
from oauth.bitbucket import (
    get_bitbucket_refresh_token,
)
from oauth.github import (
    get_access_token,
)
from oauth.gitlab import (
    get_refresh_token,
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
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            OauthBitbucketSecret,
        )

        return await gitlab.authorize_redirect(request, url)

    return RedirectResponse(url="/home")


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
        params = {"subject": organization_id}
        url = f"{redirect}?{urlencode(params)}"
        token_data: Optional[dict] = await get_refresh_token(
            code=code,
            redirect_uri=url,
            code_verifier=request.session.get(
                "_gitlab_authlib_code_verifier_", ""
            ),
        )
        if not token_data:
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
                refresh_token=token_data["refresh_token"],
                redirect_uri=url,
                access_token=token_data["access_token"],
                valid_until=get_plus_delta(
                    datetime.utcfromtimestamp(token_data["created_at"]),
                    seconds=token_data["expires_in"],
                ),
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
                loaders,
                credential.organization_id,
                credential.owner,
                OauthGitlabSecret,
            ),
        )
    )
    await credentials_model.add(credential=credential)
    organization: Organization = await loaders.organization.load(
        organization_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def do_github_oauth(request: Request) -> Response:
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    if not await has_access(
        loaders=get_new_context(),
        email=email,
        organization_id=organization_id,
    ):
        raise PermissionError("Access denied")

    redirect_uri = get_redirect_url(request, "oauth_github")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}".replace(
        "localhost", "127.0.0.1"
    )
    github = ROAUTH.create_client("github")
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            OauthBitbucketSecret,
        )

        return await github.authorize_redirect(request, url)

    return RedirectResponse(url="/home")


async def oauth_github(request: Request) -> RedirectResponse:
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

        token: Optional[str] = await get_access_token(code=code)
        if not token:
            raise OAuthError()
    except (ConnectTimeout, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    loaders: Dataloaders = get_new_context()
    name = f'Github OAUTH {str(uuid.uuid4()).split("-", maxsplit=1)[0]}'
    credential = Credentials(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=OauthGithubSecret(
                access_token=token,
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
                loaders,
                credential.organization_id,
                credential.owner,
                OauthGithubSecret,
            ),
        )
    )
    await credentials_model.add(credential=credential)
    organization: Organization = await loaders.organization.load(
        organization_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def do_bitbucket_oauth(request: Request) -> Response:
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    if not await has_access(
        loaders=get_new_context(),
        email=email,
        organization_id=organization_id,
    ):
        raise PermissionError("Access denied")

    redirect_uri = get_redirect_url(request, "oauth_bitbucket")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}"
    bitbucket = ROAUTH.create_client("bitbucket_repository")
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            OauthBitbucketSecret,
        )

        return await bitbucket.authorize_redirect(request, url)

    return RedirectResponse(url="/home")


async def oauth_bitbucket(request: Request) -> RedirectResponse:
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
        redirect = get_redirect_url(request, "oauth_bitbucket")
        token: Optional[str] = await get_bitbucket_refresh_token(
            code=code,
            subject=organization_id,
            redirect_uri=redirect,
        )
        if not token:
            raise OAuthError()
    except (ConnectTimeout, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    loaders: Dataloaders = get_new_context()
    name = f'BitBucket OAUTH {str(uuid.uuid4()).split("-", maxsplit=1)[0]}'
    credential = Credentials(
        id=(str(uuid.uuid4())),
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=OauthBitbucketSecret(
                brefresh_token=token,
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
                loaders,
                credential.organization_id,
                credential.owner,
                OauthBitbucketSecret,
            ),
        )
    )
    await credentials_model.add(credential=credential)
    organization: Organization = await loaders.organization.load(
        organization_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")
