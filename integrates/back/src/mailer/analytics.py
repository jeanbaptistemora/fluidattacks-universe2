# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .common import (
    GENERAL_TAG,
    send_mails_async,
)
from context import (
    BASE_URL,
)
from typing import (
    Any,
)


async def send_mail_analytics(
    loaders: Any, *email_to: str, **context: str
) -> None:
    mail_content = context
    mail_content["live_report_url"] = (
        f'{BASE_URL}/{mail_content["report_entity_percent"]}s/'
        f'{mail_content["report_subject_percent"]}/analytics'
    )
    await send_mails_async(
        loaders,
        list(email_to),
        mail_content,
        GENERAL_TAG,
        (
            f'[ARM] Analytics for [{mail_content["report_subject_title"]}] '
            f'({mail_content["frequency_title"]}: {mail_content["date"]})'
        ),
        "charts_report",
    )
