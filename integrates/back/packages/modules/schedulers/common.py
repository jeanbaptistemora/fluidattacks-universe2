# Standard libraries
from typing import (
    Callable,
    List
)

# Third-party libraries
from aioextensions import schedule

# Local libraries
from backend.typing import MailContent as MailContentType


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType
) -> None:
    schedule(
        send_mail_function(mail_to, mail_context)
    )
