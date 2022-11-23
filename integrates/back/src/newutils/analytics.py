from aioextensions import (
    in_thread,
)
from context import (
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from decimal import (
    Decimal,
    InvalidOperation,
)
from mixpanel import (
    Mixpanel,
)
from settings import (
    MIXPANEL_API_TOKEN,
)


def is_decimal(num: str) -> bool:
    try:
        Decimal(num)
        return True
    except InvalidOperation:
        with suppress(InvalidOperation):
            Decimal(num[:-1])
            return True
        return False


async def mixpanel_track(email: str, event: str, **extra: str) -> None:
    if FI_ENVIRONMENT == "production":
        await in_thread(
            Mixpanel(MIXPANEL_API_TOKEN).track,
            email,
            event,
            {"integrates_user_email": email, **extra},
        )
