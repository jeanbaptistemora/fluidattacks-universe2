from .enums import (
    Channel,
)
from aioextensions import (
    in_thread,
)
from context import (
    FI_TWILIO_ACCOUNT_SID,
    FI_TWILIO_AUTH_TOKEN,
    FI_TWILIO_VERIFY_SERVICE_SID,
)
from custom_exceptions import (
    CouldNotStartUserVerification,
)
from twilio.base.exceptions import (
    TwilioRestException,
)
from twilio.rest import (
    Client,
)

# Initialize Twilio client
client = Client(FI_TWILIO_ACCOUNT_SID, FI_TWILIO_AUTH_TOKEN)


async def start_verification(
    phone_number: str, channel: Channel = Channel.SMS
) -> str:
    try:
        verification = await in_thread(
            client.verify.services(
                FI_TWILIO_VERIFY_SERVICE_SID
            ).verifications.create,
            to=phone_number,
            channel=channel.value.lower(),
        )
    except TwilioRestException as exc:
        raise CouldNotStartUserVerification from exc

    return verification.sid
