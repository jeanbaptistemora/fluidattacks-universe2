from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from dataloaders import (
    Dataloaders,
)
from newutils.datetime import (
    get_now_plus_delta,
)


async def send_mail_deprecation_notice(
    *,
    loaders: Dataloaders,
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
        email_to=list(email_to),
        context=email_context,
        tags=GENERAL_TAG,
        subject=f"[ARM] {month} Deprecation Notice",
        template_name="deprecation_notice",
    )
