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
    CouldNotVerifyUser,
    InvalidVerificationCode,
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


async def check_verification(verification_sid: str, code: str) -> None:
    try:
        verification_check = await in_thread(
            client.verify.services(
                FI_TWILIO_VERIFY_SERVICE_SID
            ).verification_checks.create,
            verification_sid=verification_sid,
            code=code,
        )
    except TwilioRestException as exc:
        raise CouldNotVerifyUser from exc

    if verification_check.status != "approved":
        raise InvalidVerificationCode
