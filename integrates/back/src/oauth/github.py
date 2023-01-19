import aiohttp
import asyncio
from context import (
    FI_GITHUB_OAUTH2_APP_ID,
    FI_GITHUB_OAUTH2_SECRET,
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

# Constants
LOGGER = logging.getLogger(__name__)
GITHUB_AUTHZ_URL = "https://github.com/login/oauth/authorize"
GITHUB_REFRESH_URL = "https://github.com/login/oauth/access_token"

GITHUB_ARGS = dict(
    name="github",
    client_id=FI_GITHUB_OAUTH2_APP_ID,
    authorize_url=GITHUB_AUTHZ_URL,
    client_kwargs={"scope": "read:org repo"},
)


async def get_access_token(
    *,
    code: str,
) -> Optional[str]:
    request_parameters: dict[str, str] = dict(
        client_id=FI_GITHUB_OAUTH2_APP_ID,
        client_secret=FI_GITHUB_OAUTH2_SECRET,
        code=code,
    )
    headers: dict[str, str] = {
        "Accept": "application/json",
        "content-type": "application/json",
    }
    retries: int = 0
    retry: bool = True
    async with aiohttp.ClientSession(headers=headers) as session:
        while retry and retries < 10:
            async with session.post(
                GITHUB_REFRESH_URL,
                data=json.dumps(request_parameters),
            ) as response:
                try:
                    result = await response.json()
                except (
                    json.decoder.JSONDecodeError,
                    aiohttp.ClientError,
                ) as exc:
                    LOGGER.exception(exc, extra=dict(extra=locals()))
                    break
                if not response.ok:
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.2)
                    continue

                return result["access_token"]

    return None
