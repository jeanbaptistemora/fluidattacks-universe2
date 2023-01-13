from aiohttp import (
    BasicAuth,
    ClientSession,
    FormData,
)
from aiohttp.client_exceptions import (
    ClientError,
)
import asyncio
from context import (
    FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
    FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
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
from urllib.parse import (
    urlencode,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BITBUCKET_REFRESH_URL = "https://bitbucket.org/site/oauth2/access_token"
BITBUCKET_AUTHZ_URL = "https://bitbucket.org/site/oauth2/authorize"

BITBUCKET_REPOSITORY_ARGS = dict(
    name="bitbucket_repository",
    authorize_url=BITBUCKET_AUTHZ_URL,
    client_id=FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
    client_secret=FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
    client_kwargs={"scope": "repository"},
)


async def get_bitbucket_refresh_token(
    *,
    code: str,
    subject: str,
    redirect_uri: str,
) -> Optional[str]:
    params = {"subject": subject}
    url = f"{redirect_uri}?{urlencode(params)}"
    request_parameters: dict[str, str] = dict(
        code=code,
        grant_type="authorization_code",
        redirect_uri=url,
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
                BITBUCKET_REFRESH_URL,
                data=data,
                auth=BasicAuth(
                    login=FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
                    password=FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET,
                ),
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

                return result["refresh_token"]

    return None
