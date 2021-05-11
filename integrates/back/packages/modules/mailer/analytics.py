
from typing import cast

from __init__ import BASE_URL
from custom_types import MailContent as MailContentType

from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


async def send_mail_analytics(
    *email_to: str,
    **context: str
) -> None:
    context = cast(MailContentType, context)
    context['live_report_url'] = (
        f'{BASE_URL}/{context["report_entity_percent"]}s/'
        f'{context["report_subject_percent"]}'
    )
    await send_mails_async_new(
        list(email_to),
        context,
        GENERAL_TAG,
        (
            f'Analytics for [{context["report_subject_title"]}] '
            f'({context["frequency_title"]}: {context["date"]})'
        ),
        'charts_report'
    )
