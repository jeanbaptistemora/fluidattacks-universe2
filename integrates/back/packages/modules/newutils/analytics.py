from aioextensions import in_thread
from mixpanel import Mixpanel

from back import settings
from __init__ import FI_ENVIRONMENT


async def mixpanel_track(email: str, event: str, **extra: str) -> None:
    if FI_ENVIRONMENT == 'production':
        await in_thread(
            Mixpanel(settings.MIXPANEL_API_TOKEN).track,
            email,
            event,
            {'integrates_user_email': email, **extra}
        )
