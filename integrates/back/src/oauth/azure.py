from aiohttp import (
    ClientSession,
    FormData,
)
from aiohttp.client_exceptions import (
    ClientError,
)
import asyncio
from context import (
    FI_AZURE_OAUTH2_REPOSITORY_APP_ID,
    FI_AZURE_OAUTH2_REPOSITORY_SECRET,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthAzureSecret,
)
from db_model.credentials.update import (
    update_credential_state,
)
import json
import logging
import logging.config
from newutils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
import pytz
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
AZURE_REFRESH_URL = "https://app.vssps.visualstudio.com/oauth2/token"
AZURE_AUTHZ_URL = "https://app.vssps.visualstudio.com/oauth2/authorize"

AZURE_REPOSITORY_ARGS = dict(
    name="azure_repository",
    response_type="Assertion",
    authorize_url=AZURE_AUTHZ_URL,
    client_id=FI_AZURE_OAUTH2_REPOSITORY_APP_ID,
    client_kwargs={"scope": "vso.project vso.code"},
)


async def get_azure_refresh_token(
    *,
    code: str,
    redirect_uri: str,
) -> dict | None:
    request_parameters: dict[str, str] = dict(
        client_assertion_type=(
            "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
        ),
        client_assertion=FI_AZURE_OAUTH2_REPOSITORY_SECRET,
        grant_type="urn:ietf:params:oauth:grant-type:jwt-bearer",
        assertion=code,
        redirect_uri=redirect_uri,
    )
    data = FormData()
    for key, value in request_parameters.items():
        data.add_field(key, value)
    retries: int = 0
    retry: bool = True
    async with ClientSession() as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                AZURE_REFRESH_URL,
                data=data,
            ) as response:
                try:
                    result = await response.json()
                except (
                    json.decoder.JSONDecodeError,
                    ClientError,
                ) as exc:
                    LOGGER.exception(exc, extra=dict(extra=locals()))
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                return result

    return None


async def get_azure_token(
    *,
    credential: Credentials,
    loaders: Dataloaders,
) -> str | None:
    if not isinstance(credential.state.secret, OauthAzureSecret):
        return None

    request_parameters: dict[str, str] = dict(
        client_assertion_type=(
            "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
        ),
        grant_type="refresh_token",
        client_assertion=FI_AZURE_OAUTH2_REPOSITORY_SECRET,
        assertion=credential.state.secret.arefresh_token,
        redirect_uri=credential.state.secret.redirect_uri,
    )
    data = FormData()
    for key, value in request_parameters.items():
        data.add_field(key, value)
    retries: int = 0
    retry: bool = True
    async with ClientSession(
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ) as session:
        while retry and retries < 5:
            retry = False
            async with session.post(
                AZURE_REFRESH_URL,
                data=data,
            ) as response:
                try:
                    result = await response.json()
                except (
                    json.decoder.JSONDecodeError,
                    ClientError,
                ) as exc:
                    LOGGER.exception(exc, extra=dict(extra=locals()))
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
                    secret=OauthAzureSecret(
                        redirect_uri=credential.state.secret.redirect_uri,
                        arefresh_token=result["refresh_token"],
                        access_token=result["access_token"],
                        valid_until=get_plus_delta(
                            get_minus_delta(get_utc_now(), seconds=60),
                            seconds=int(result["expires_in"]),
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
