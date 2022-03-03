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
    InvalidMobileNumber,
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
            rate_limits={"end_user_phone_number": phone_number},
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


async def validate_mobile(phone_number: str) -> None:
    try:
        phone_info = await in_thread(
            client.lookups.v1.phone_numbers(phone_number=phone_number).fetch,
            type=["carrier"],
        )
    except TwilioRestException as exc:
        raise InvalidMobileNumber from exc

    if phone_info.carrier["type"] != "mobile":
        raise InvalidMobileNumber
