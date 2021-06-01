from aioextensions import (
    schedule,
)
from custom_types import (
    MailContent as MailContentType,
)
from typing import (
    Callable,
    List,
)


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType,
) -> None:
    schedule(send_mail_function(mail_to, mail_context))
