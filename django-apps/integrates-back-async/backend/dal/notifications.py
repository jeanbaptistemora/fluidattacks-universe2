# Standard library
import contextlib

# Third party imports
import rollbar
from zenpy import Zenpy
from zenpy.lib.exception import ZenpyException
from zenpy.lib.api_objects import Ticket, User

# Local imports
from __init__ import (
    FI_ZENDESK_EMAIL,
    FI_ZENDESK_SUBDOMAIN,
    FI_ZENDESK_TOKEN,
)


@contextlib.contextmanager
def zendesk() -> Zenpy:
    try:
        yield Zenpy(
            email=FI_ZENDESK_EMAIL,
            subdomain=FI_ZENDESK_SUBDOMAIN,
            token=FI_ZENDESK_TOKEN,
        )
    except ZenpyException as exception:
        rollbar.report_exc_info()
        raise exception


def create_ticket(
    *,
    subject: str,
    description: str,
    requester_email: str,
) -> bool:
    success: bool = False

    try:

        with zendesk() as api:
            api.tickets.create(Ticket(
                subject=subject,
                description=description,
                requester=User(
                    name=requester_email,
                    email=requester_email,
                ),
            ))

    except ZenpyException:
        rollbar.report_exc_info()
    else:
        success = True
        rollbar.report_message(
            'Zendesk ticket created',
            level='debug',
            extra_data=dict(
                subject=subject,
                description=description,
                requester_email=requester_email,
            ),
        )

    return success
