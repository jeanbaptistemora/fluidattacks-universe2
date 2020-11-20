# Standard library
import contextlib
import logging

# Third party imports
import requests
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushResponseError,
    PushServerError
)
from zenpy import Zenpy
from zenpy.lib.exception import ZenpyException
from zenpy.lib.api_objects import Ticket, User

# Local imports
from fluidintegrates.settings import LOGGING
from __init__ import (
    FI_ZENDESK_EMAIL,
    FI_ZENDESK_SUBDOMAIN,
    FI_ZENDESK_TOKEN,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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

    except ZenpyException as exception:
        LOGGER.exception(exception, extra=dict(extra=locals()))
    else:
        success = True
        LOGGER.info(
            'Zendesk ticket created',
            extra={
                'extra': dict(
                    subject=subject,
                    description=description,
                    requester_email=requester_email,
                )
            })

    return success


def send_push_notification(
    user_email: str,
    token: str,
    title: str,
    message: str
) -> None:
    client = PushClient()

    try:
        response = client.publish(
            PushMessage(
                body=message,
                channel_id='default',
                data={'message': message, 'title': title},
                display_in_foreground=True,
                priority='high',
                sound='default',
                title=title,
                to=token,
            )
        )
        LOGGER.info(
            '[notifier]: push notification sent',
            extra={
                'extra': {
                    'email': user_email,
                    'title': title,
                }
            })
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        PushServerError
    ) as ex:
        LOGGER.exception(ex)

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        raise
    except PushResponseError as ex:
        LOGGER.exception(ex)
