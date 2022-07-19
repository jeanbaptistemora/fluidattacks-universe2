from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from datetime import (
    datetime,
)
from newutils.datetime import (
    get_now_plus_delta,
)
from typing import (
    Any,
)


async def send_mail_deprecation_notice(
    *,
    loaders: Any,
    deprecations: dict[str, str],
    email_to: list[str],
) -> None:
    # These mails are meant to anticipate next month's deprecations
    date: datetime = get_now_plus_delta(weeks=4)
    month: str = date.strftime("%B")
    email_context: dict[str, dict[str, str]] = {
        "deprecations": deprecations,
    }
    await send_mails_async(
        loaders,
        email_to,
        email_context,
        GENERAL_TAG,
        f"[ASM] {month} Deprecation Notice",
        "deprecation_notice",
    )
