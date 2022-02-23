from aioextensions import (
    schedule,
)
from custom_types import (
    MailContent as MailContentType,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Callable,
    List,
)

# FP: local testing
logging.config.dictConfig(LOGGING)  # NOSONAR
LOGGER_CONSOLE = logging.getLogger("console")


def info(*args: Any, extra: Any = None) -> None:
    LOGGER_CONSOLE.info(*args, extra=dict(extra=extra))


def error(*args: Any, extra: Any = None) -> None:
    LOGGER_CONSOLE.error(*args, extra=dict(extra=extra))


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType,
) -> None:
    schedule(send_mail_function(mail_to, mail_context))
