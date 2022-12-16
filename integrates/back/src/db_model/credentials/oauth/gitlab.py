import aiohttp
import asyncio
from context import (
    FI_GITLAB_OAUTH2_APP_ID,
    FI_GITLAB_OAUTH2_SECRET,
)
import json
from typing import (
    Optional,
)
from urllib.parse import (
    urlencode,
)

GITLAB_AUTHZ_URL = "https://gitlab.com/oauth/authorize"
GITLAB_REFRESH_URL = "https://gitlab.com/oauth/token"

GITLAB_ARGS = dict(
    name="gitlab",
    client_id=FI_GITLAB_OAUTH2_APP_ID,
    client_secret=FI_GITLAB_OAUTH2_SECRET,
    authorize_url=GITLAB_AUTHZ_URL,
    client_kwargs={"scope": "read_repository"},
)


async def get_refresh_token(
    *, code: str, subject: str, redirect_uri: str
) -> Optional[str]:
    params = {"subject": subject}
    url = f"{redirect_uri}?{urlencode(params)}"
    request_parameters: dict[str, str] = dict(
        client_id=FI_GITLAB_OAUTH2_APP_ID,
        client_secret=FI_GITLAB_OAUTH2_SECRET,
        code=code,
        grant_type="authorization_code",
        redirect_uri=url,
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

                return result["refresh_token"]

    return None
