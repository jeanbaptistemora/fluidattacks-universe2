from .common import (
    GENERAL_TAG,
    send_mails_async,
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
    mail_deprecations: dict[str, str],
    email_to: set[str],
) -> None:
    # These mails are meant to anticipate next month's deprecations
    month: str = get_now_plus_delta(weeks=4).strftime("%B")
    email_context: dict[str, dict[str, str]] = {
        "deprecations": mail_deprecations,
    }
    await send_mails_async(
        loaders,
        list(email_to),
        email_context,
        GENERAL_TAG,
        f"[ASM] {month} Deprecation Notice",
        "deprecation_notice",
    )
