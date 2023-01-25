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
import json
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
AZURE_REFRESH_URL = "https://app.vssps.visualstudio.com/oauth2/token"
AZURE_AUTHZ_URL = "https://bitbucket.org/site/oauth2/authorize"

AZURE_REPOSITORY_ARGS = dict(
    name="azure_repository",
    authorize_url=AZURE_AUTHZ_URL,
    client_id=FI_AZURE_OAUTH2_REPOSITORY_APP_ID,
    client_kwargs={"scope": "vso.project vso.code"},
)


async def get_azure_refresh_token(
    *,
    code: str,
    redirect_uri: str,
) -> Optional[dict]:
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
