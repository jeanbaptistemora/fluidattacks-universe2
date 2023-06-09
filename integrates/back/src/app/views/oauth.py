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
from authz.enforcer import (
    get_organization_level_enforcer,
)
from batch.dal import (
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
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
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
from httpx import (
    ConnectTimeout,
)
import json
import logging
import logging.config
from newutils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
from oauth import (
    OAUTH as ROAUTH,
)
from oauth.azure import (
    get_azure_refresh_token,
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
from organization_access import (
    domain as orgs_access,
)
from organizations.utils import (
    get_organization,
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
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    parse_qs,
    urlencode,
)
import uuid

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def _validate(
    *,
    loaders: Dataloaders,
    email: str,
    organization_id: str,
) -> None:
    enforcer = await get_organization_level_enforcer(loaders, email)
    if not enforcer(
        organization_id, "api_mutations_add_credentials_mutate"
    ) or not await orgs_access.has_access(
        loaders=loaders,
        email=email,
        organization_id=organization_id,
    ):
        raise PermissionError("Access denied")


async def _put_action(
    *,
    organization_id: str,
    credentials_id: str,
) -> None:
    await put_action(
        action=Action.UPDATE_ORGANIZATION_REPOSITORIES,
        vcpus=2,
        product_name=Product.INTEGRATES,
        queue=IntegratesBatchQueue.SMALL,
        additional_info=json.dumps({"credentials_id": credentials_id}),
        entity=organization_id.lower().lstrip("org#"),
        attempt_duration_seconds=7200,
        subject="integrates@fluidattacks.com",
    )


async def do_gitlab_oauth(request: Request) -> Response:
    loaders: Dataloaders = get_new_context()
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    await _validate(
        loaders=loaders, email=email, organization_id=organization_id
    )
    redirect_uri = get_redirect_url(request, "oauth_gitlab")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}"
    gitlab = ROAUTH.create_client("gitlab")
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            OauthGitlabSecret,
        )

        return await gitlab.authorize_redirect(request, url)

    return RedirectResponse(url="/home")


async def oauth_gitlab(
    request: Request,
) -> RedirectResponse:
    try:
        loaders: Dataloaders = get_new_context()
        user_info = await get_jwt_content(request)
        try:
            organization_id: str = request.query_params["subject"]
            code: str = request.query_params["code"]
        except KeyError as ex:
            LOGGER.exception(ex, extra=dict(extra=locals()))
            return RedirectResponse(url="/home")

        await _validate(
            loaders=loaders,
            email=user_info["user_email"],
            organization_id=organization_id,
        )

        redirect = get_redirect_url(request, "oauth_gitlab")
        params = {"subject": organization_id}
        url = f"{redirect}?{urlencode(params)}"
        token_data: dict | None = await get_refresh_token(
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

    name = f'{str(user_info["user_email"]).split("@", maxsplit=1)[0]}(GitLab)'
    credentials_id: str = str(uuid.uuid4())
    credential = Credentials(
        id=credentials_id,
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
    organization = await get_organization(loaders, organization_id)
    await _put_action(
        organization_id=organization_id, credentials_id=credentials_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def do_github_oauth(request: Request) -> Response:
    loaders: Dataloaders = get_new_context()
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    await _validate(
        loaders=loaders, email=email, organization_id=organization_id
    )

    redirect_uri = get_redirect_url(request, "oauth_github")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}"
    github = ROAUTH.create_client("github")
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            OauthGithubSecret,
        )

        return await github.authorize_redirect(request, url)

    return RedirectResponse(url="/home")


async def oauth_github(request: Request) -> RedirectResponse:
    try:
        loaders: Dataloaders = get_new_context()
        user_info = await get_jwt_content(request)
        email: str = user_info["user_email"]
        try:
            organization_id: str = request.query_params["subject"]
            code: str = request.query_params["code"]
        except KeyError as exc:
            LOGGER.exception(exc, extra=dict(extra=locals()))
            return RedirectResponse(url="/home")

        enforcer = await get_organization_level_enforcer(loaders, email)
        if not enforcer(
            organization_id, "api_mutations_add_credentials_mutate"
        ) or not await orgs_access.has_access(
            loaders=loaders,
            email=email,
            organization_id=organization_id,
        ):
            raise PermissionError("Access denied")

        token: str | None = await get_access_token(code=code)
        if not token:
            raise OAuthError()
    except (ConnectTimeout, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    name = f'{str(user_info["user_email"]).split("@", maxsplit=1)[0]}(GitHub)'
    credentials_id: str = str(uuid.uuid4())
    credential = Credentials(
        id=credentials_id,
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
    organization = await get_organization(loaders, organization_id)
    await _put_action(
        organization_id=organization_id, credentials_id=credentials_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def do_bitbucket_oauth(request: Request) -> Response:
    loaders: Dataloaders = get_new_context()
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    await _validate(
        loaders=loaders, email=email, organization_id=organization_id
    )

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
        loaders: Dataloaders = get_new_context()
        user_info = await get_jwt_content(request)
        email: str = user_info["user_email"]
        organization_id: str = request.query_params["subject"]
        code: str = request.query_params["code"]
        await _validate(
            loaders=loaders, email=email, organization_id=organization_id
        )
        redirect = get_redirect_url(request, "oauth_bitbucket")
        token_data: dict | None = await get_bitbucket_refresh_token(
            code=code,
            subject=organization_id,
            redirect_uri=redirect,
        )
        if not token_data:
            raise OAuthError()
    except (KeyError, ConnectTimeout, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    name = (
        f'{str(user_info["user_email"]).split("@", maxsplit=1)[0]}(Bitbucket)'
    )
    credentials_id: str = str(uuid.uuid4())
    credential = Credentials(
        id=credentials_id,
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=OauthBitbucketSecret(
                brefresh_token=token_data["refresh_token"],
                access_token=token_data["access_token"],
                valid_until=get_plus_delta(
                    get_minus_delta(get_utc_now(), seconds=60),
                    seconds=int(token_data["expires_in"]),
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
                OauthBitbucketSecret,
            ),
        )
    )
    await credentials_model.add(credential=credential)
    organization = await get_organization(loaders, organization_id)
    await _put_action(
        organization_id=organization_id, credentials_id=credentials_id
    )

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def do_azure_oauth(request: Request) -> Response:
    loaders: Dataloaders = get_new_context()
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    await _validate(
        loaders=loaders,
        email=user_info["user_email"],
        organization_id=organization_id,
    )

    redirect_uri = get_redirect_url(request, "oauth_azure")
    params = {"subject": organization_id}
    url = f"{redirect_uri}?{urlencode(params)}"
    request.session["azure_repository_authlib_redirect_uri"] = url
    azure = ROAUTH.create_client("azure_repository")
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            user_info["user_email"],
            OauthAzureSecret,
        )

        return await azure.authorize_redirect(request, redirect_uri)

    return RedirectResponse(url="/home")


async def oauth_azure(
    request: Request,
) -> RedirectResponse:
    try:
        loaders: Dataloaders = get_new_context()
        user_info = await get_jwt_content(request)
        organization_id: str = parse_qs(
            parse_url(
                request.session.get(
                    "azure_repository_authlib_redirect_uri", ""
                )
            ).query
        )["subject"][0]
        code: str = request.query_params["code"]
        await _validate(
            loaders=loaders,
            email=user_info["user_email"],
            organization_id=organization_id,
        )
        redirect = get_redirect_url(request, "oauth_azure")
        token_data: dict | None = await get_azure_refresh_token(
            code=code,
            redirect_uri=redirect,
        )
        if not token_data:
            raise OAuthError()
    except (ConnectTimeout, KeyError, MismatchingStateError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = RedirectResponse(url="/home")
        return response

    name = f'{str(user_info["user_email"]).split("@", maxsplit=1)[0]}(Azure)'
    credentials_id: str = str(uuid.uuid4())
    credential = Credentials(
        id=credentials_id,
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=OauthAzureSecret(
                arefresh_token=token_data["refresh_token"],
                redirect_uri=redirect,
                access_token=token_data["access_token"],
                valid_until=get_plus_delta(
                    get_minus_delta(get_utc_now(), seconds=60),
                    seconds=int(token_data["expires_in"]),
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
                OauthAzureSecret,
            ),
        )
    )
    await credentials_model.add(credential=credential)
    organization = await get_organization(loaders, organization_id)
    await _put_action(
        organization_id=organization_id, credentials_id=credentials_id
    )
    request.session.pop("azure_repository_authlib_redirect_uri")

    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")
