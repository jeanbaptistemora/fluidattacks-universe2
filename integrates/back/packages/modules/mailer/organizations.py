# Standard libraries
from typing import List

# Third-party libraries

# Local libraries
from backend.typing import MailContent as MailContentType
from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


async def send_mail_org_deletion(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Organization deletion [{context["org_name"]}]',
        'organization_deletion'
    )
