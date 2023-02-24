from aioextensions import (
    collect,
    in_thread,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
    FI_TWILIO_ACCOUNT_SID,
    FI_TWILIO_AUTH_TOKEN,
)
from custom_exceptions import (
    UnableToSendSms,
)
from twilio.base.exceptions import (
    TwilioRestException,
)
from twilio.rest import (
    Client,
)
from typing import (
    Any,
)

# Initialize Twilio client
client = Client(FI_TWILIO_ACCOUNT_SID, FI_TWILIO_AUTH_TOKEN)


async def send_sms_notification(
    *,
    phone_number: str,
    message_body: str,
) -> None:
    if FI_ENVIRONMENT == "development":
        return
    try:
        await in_thread(
            client.messages.create,
            to=phone_number,
            from_="",
            body=message_body,
        )
    except TwilioRestException as exc:
        raise UnableToSendSms() from exc


async def send_sms_notifications(
    *,
    phone_numbers: list[str],
    context: dict[str, Any],
) -> None:
    test_group_list = FI_TEST_PROJECTS.split(",")
    await collect(
        tuple(
            send_sms_notification(
                phone_number=phone_number,
                message_body=context["message_body"],
            )
            for phone_number in phone_numbers
            if (
                str(context.get("group", "")).lower() not in test_group_list
                and context.get("message_body")
            )
        )
    )
