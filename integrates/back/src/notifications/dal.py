from context import (
    FI_ZENDESK_EMAIL,
    FI_ZENDESK_SUBDOMAIN,
    FI_ZENDESK_TOKEN,
)
import contextlib
import logging
import logging.config
from settings import (
    LOGGING,
)
from zenpy import (
    Zenpy,
)
from zenpy.lib.api_objects import (
    Ticket,
    User,
)
from zenpy.lib.exception import (
    ZenpyException,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


def create_ticket(
    *,
    subject: str,
    description: str,
    requester_email: str,
) -> bool:
    success: bool = False
    try:
        with zendesk() as api:
            api.tickets.create(
                Ticket(
                    subject=subject,
                    description=description,
                    requester=User(
                        name=requester_email,
                        email=requester_email,
                    ),
                )
            )
    except ZenpyException as exception:
        LOGGER.exception(exception, extra=dict(extra=locals()))
    else:
        success = True
        LOGGER_TRANSACTIONAL.info(
            ": ".join((requester_email, "Zendesk ticket created")),
            extra={
                "extra": dict(
                    subject=subject,
                    description=description,
                    requester_email=requester_email,
                )
            },
        )
    return success


@contextlib.contextmanager
def zendesk() -> Zenpy:
    try:
        yield Zenpy(
            email=FI_ZENDESK_EMAIL,
            subdomain=FI_ZENDESK_SUBDOMAIN,
            token=FI_ZENDESK_TOKEN,
        )
    except ZenpyException as exception:
        LOGGER.exception(exception, extra=dict(extra=locals()))
        raise exception
