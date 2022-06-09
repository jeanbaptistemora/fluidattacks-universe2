import aiohttp
import logging

LOGGER = logging.getLogger(__name__)


async def is_personal_email(user_email: str) -> bool:
    url = (
        "https://gist.githubusercontent.com/tbrianjones/5992856/raw/"
        "93213efb652749e226e69884d6c048e595c1280a/"
        "free_email_provider_domains.txt"
    )
    email_domain = user_email.split("@")[1]
    error_msg = "Couldn't fetch free email provider domains"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    free_email_domains = text.split("\n")

                    return email_domain in free_email_domains

                LOGGER.error(error_msg, response)
                return True
    except aiohttp.ClientError as exception:
        LOGGER.error(error_msg, exception)
        return True
