from context import (
    FI_ZENDESK_EMAIL,
    FI_ZENDESK_SUBDOMAIN,
    FI_ZENDESK_TOKEN,
)
import contextlib
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushResponse,
    PushResponseError,
    PushServerError,
)
import logging
import logging.config
import requests
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


def send_push_notification(
    user_email: str, token: str, title: str, message: str
) -> None:
    client = PushClient()
    try:
        response: PushResponse = client.publish(
            PushMessage(
                body=message,
                channel_id="default",
                data={"message": message, "title": title},
                display_in_foreground=True,
                priority="high",
                sound="default",
                title=title,
                to=token,
            )
        )
        try:
            response.validate_response()
            LOGGER_TRANSACTIONAL.info(
                ": ".join(
                    (
                        user_email,
                        "[notifier]: push notification sent successfully",
                    )
                ),
                extra={
                    "extra": {
                        "email": user_email,
                        "title": title,
                    }
                },
            )
        except DeviceNotRegisteredError:
            raise
        except PushResponseError as ex:
            LOGGER.exception(ex)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        PushServerError,
    ) as ex:
        LOGGER.exception(ex)


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
