import aiohttp
import asyncio
from context import (
    FI_GITLAB_OAUTH2_APP_ID,
    FI_GITLAB_OAUTH2_SECRET,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthGitlabSecret,
)
from db_model.credentials.update import (
    update_credential_state,
)
import json
import pytz

GITLAB_AUTHZ_URL = "https://gitlab.com/oauth/authorize"
GITLAB_REFRESH_URL = "https://gitlab.com/oauth/token"

GITLAB_ARGS = dict(
    name="gitlab",
    client_id=FI_GITLAB_OAUTH2_APP_ID,
    client_secret=FI_GITLAB_OAUTH2_SECRET,
    authorize_url=GITLAB_AUTHZ_URL,
    code_challenge_method="S256",
    client_kwargs={"scope": "read_api read_repository"},
)


async def get_refresh_token(
    *,
    code: str,
    redirect_uri: str,
    code_verifier: str,
) -> dict | None:
    request_parameters: dict[str, str] = dict(
        client_id=FI_GITLAB_OAUTH2_APP_ID,
        client_secret=FI_GITLAB_OAUTH2_SECRET,
        code=code,
        grant_type="authorization_code",
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    headers: dict[str, str] = {"content-type": "application/json"}
    retries: int = 0
    retry: bool = True
    async with aiohttp.ClientSession(headers=headers) as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                GITLAB_REFRESH_URL,
                data=json.dumps(request_parameters),
            ) as response:
                try:
                    result = await response.json()
                except json.decoder.JSONDecodeError:
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                return result

    return None


async def get_token(
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> str | None:
    if not isinstance(credential.state.secret, OauthGitlabSecret):
        return None

    request_parameters: dict[str, str] = dict(
        client_id=FI_GITLAB_OAUTH2_APP_ID,
        client_secret=FI_GITLAB_OAUTH2_SECRET,
        refresh_token=credential.state.secret.refresh_token,
        grant_type="refresh_token",
        redirect_uri=credential.state.secret.redirect_uri,
    )
    headers: dict[str, str] = {"content-type": "application/json"}
    retries: int = 0
    retry: bool = True
    async with aiohttp.ClientSession(headers=headers) as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                GITLAB_REFRESH_URL,
                data=json.dumps(request_parameters),
            ) as response:
                try:
                    result = await response.json()
                except json.decoder.JSONDecodeError:
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                new_state = CredentialsState(
                    modified_by=credential.state.modified_by,
                    modified_date=datetime.now(tz=pytz.timezone("UTC")),
                    name=credential.state.name,
                    secret=OauthGitlabSecret(
                        redirect_uri=credential.state.secret.redirect_uri,
                        refresh_token=result["refresh_token"],
                        access_token=result["access_token"],
                        valid_until=(
                            datetime.utcfromtimestamp(result["created_at"])
                            + timedelta(seconds=int(result["expires_in"]))
                        ),
                    ),
                    is_pat=credential.state.is_pat,
                    azure_organization=credential.state.azure_organization,
                    type=credential.state.type,
                )
                await update_credential_state(
                    current_value=credential.state,
                    credential_id=credential.id,
                    organization_id=credential.organization_id,
                    state=new_state,
                    force_update_owner=False,
                )
                loaders.credentials.clear_all()
                loaders.organization_credentials.clear(
                    credential.organization_id
                )

                return result["access_token"]

    return None
