from aioextensions import (
    schedule,
)
from context import (
    PRODUCT_API_TOKEN,
)
from custom_types import (
    MailContent as MailContentType,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import skims_sdk
from typing import (
    Any,
    Callable,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)
LOGGER_CONSOLE = logging.getLogger("console")


def info(*args: Any, extra: Any = None) -> None:
    LOGGER_CONSOLE.info(*args, extra=dict(extra=extra))


def error(*args: Any, extra: Any = None) -> None:
    LOGGER_CONSOLE.error(*args, extra=dict(extra=extra))


async def skims_queue(
    *,
    finding_code: Optional[str] = None,
    finding_title: Optional[str] = None,
    group_name: str,
    namespace: str,
    urgent: bool,
) -> None:
    skims_queue_kwargs = dict(
        finding_code=finding_code,
        finding_title=finding_title,
        group=group_name,
        namespace=namespace,
        urgent=urgent,
        product_api_token=PRODUCT_API_TOKEN,
    )

    info("Queueing Skims", extra=skims_queue_kwargs)
    if not await skims_sdk.queue(**skims_queue_kwargs):
        error("Could not queue a skims execution", extra=skims_queue_kwargs)


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType,
) -> None:
    schedule(send_mail_function(mail_to, mail_context))
