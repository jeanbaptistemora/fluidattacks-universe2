# Standard libraries
from typing import List

# Third-party libraries

# Local libraries
from backend.typing import MailContent as MailContentType
from .common import (
    GENERAL_TAG,
    send_mails_async_new,
)


async def send_mail_resources(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Changes in resources for [{context["project"]}]',
        'resources_changes'
    )
