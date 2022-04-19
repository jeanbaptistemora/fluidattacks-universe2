from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from custom_types import (
    MailContent as MailContentType,
)
from typing import (
    cast,
)


async def send_mail_analytics(*email_to: str, **context: str) -> None:
    mail_content = cast(MailContentType, context)
    mail_content["live_report_url"] = (
        f'{BASE_URL}/{mail_content["report_entity_percent"]}s/'
        f'{mail_content["report_subject_percent"]}/analytics'
    )
    await send_mails_async(
        list(email_to),
        mail_content,
        GENERAL_TAG,
        (
            f'Analytics for [{mail_content["report_subject_title"]}] '
            f'({mail_content["frequency_title"]}: {mail_content["date"]})'
        ),
        "charts_report",
    )
