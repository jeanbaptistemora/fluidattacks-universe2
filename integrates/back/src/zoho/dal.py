from aiohttp import (
    ClientSession,
    FormData,
)
from aiohttp.client_exceptions import (
    ClientError,
)
import asyncio
from context import (
    FI_ZOHO_SUBSCRIPTIONS_CLIENT_ID,
    FI_ZOHO_SUBSCRIPTIONS_CLIENT_SECRET,
    FI_ZOHO_SUBSCRIPTIONS_REFRESH_TOKEN,
)
import json
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)

ZOHO_SUBSCRIPTIONS_URL = "https://www.zohoapis.com/subscriptions/v1/"
ZOHO_OAUTH_TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"  # nosec
ZOHO_SUBSCRIPTIONS_REDIRECT_URI = "http://www.zoho.com/subscriptions"


async def get_access_token() -> str | None:
    request_parameters: dict[str, str] = dict(
        client_id=FI_ZOHO_SUBSCRIPTIONS_CLIENT_ID,
        client_secret=FI_ZOHO_SUBSCRIPTIONS_CLIENT_SECRET,
        grant_type="refresh_token",
        redirect_uri=ZOHO_SUBSCRIPTIONS_REDIRECT_URI,
        refresh_token=FI_ZOHO_SUBSCRIPTIONS_REFRESH_TOKEN,
    )
    headers: dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    retries: int = 0
    retry: bool = True
    data = FormData()
    for key, value in request_parameters.items():
        data.add_field(key, value)
    async with ClientSession(headers=headers) as session:
        while retry and retries < 10:
            async with session.post(
                ZOHO_OAUTH_TOKEN_URL,
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

                return result["access_token"]

    return None
