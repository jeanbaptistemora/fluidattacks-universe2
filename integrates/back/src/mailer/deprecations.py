from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from newutils.datetime import (
    get_now_plus_delta,
)
from newutils.deprecations import (
    ApiDeprecation,
)
from typing import (
    Any,
)


def _format_deprecation_for_mail(
    deprecations: dict[str, list[ApiDeprecation]]
) -> dict[str, str]:
    """
    Translates the deprecation dict values to a more readable mail format
    """
    depr_mail: dict[str, str] = {}
    for key, deprecated_fields in deprecations.items():
        depr_mail[key] = " | ".join(
            [field.field for field in deprecated_fields]
        )

    return depr_mail


async def send_mail_deprecation_notice(
    *,
    loaders: Any,
    deprecations: dict[str, list[ApiDeprecation]],
    email_to: list[str],
) -> None:
    # These mails are meant to anticipate next month's deprecations
    month: str = get_now_plus_delta(weeks=4).strftime("%B")
    email_context: dict[str, dict[str, str]] = {
        "deprecations": _format_deprecation_for_mail(deprecations),
    }
    await send_mails_async(
        loaders,
        email_to,
        email_context,
        GENERAL_TAG,
        f"[ASM] {month} Deprecation Notice",
        "deprecation_notice",
    )
