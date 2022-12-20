from aioextensions import (
    schedule,
)
from dataloaders import (
    Dataloaders,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Callable,
)

# FP: local testing
logging.config.dictConfig(LOGGING)  # NOSONAR
LOGGER = logging.getLogger(__name__)


def info(*args: Any, extra: Any = None) -> None:
    LOGGER.info(*args, extra=dict(extra=extra))


def error(*args: Any, extra: Any = None) -> None:
    LOGGER.error(*args, extra=dict(extra=extra))


def scheduler_send_mail(
    loaders: Dataloaders,
    send_mail_function: Callable,
    mail_to: list[str],
    mail_context: dict[str, Any],
) -> None:
    schedule(send_mail_function(loaders, mail_to, mail_context))
