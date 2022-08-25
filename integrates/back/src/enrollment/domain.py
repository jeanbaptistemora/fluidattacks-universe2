from aioextensions import (
    schedule,
)
from custom_exceptions import (
    EnrollmentNotFound,
    EnrollmentUserExists,
    InvalidParameter,
    UnableToSendMail,
)
from db_model import (
    enrollment as enrollment_model,
)
from db_model.enrollment.types import (
    Enrollment,
    EnrollmentMetadataToUpdate,
    Trial,
)
from decorators import (
    retry_on_exceptions,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.groups import (
    send_mail_free_trial_start,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_email_address,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

mail_free_trial_start = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_free_trial_start)


async def exists(
    loaders: Any,
    user_email: str,
) -> bool:
    try:
        enrollment: Enrollment = await loaders.enrollment.load(user_email)
        return enrollment.enrolled
    except EnrollmentNotFound:
        return False


async def add_enrollment(
    *,
    loaders: Any,
    user_email: str,
    full_name: str,
) -> None:
    validate_email_address(user_email)

    if not user_email:
        raise InvalidParameter()

    if await exists(loaders, user_email):
        raise EnrollmentUserExists.new()

    await enrollment_model.add(
        enrollment=Enrollment(
            email=user_email,
            enrolled=True,
            trial=Trial(
                completed=False,
                extension_date=datetime_utils.get_iso_date(),
                extension_days=0,
                start_date=datetime_utils.get_iso_date(),
            ),
        )
    )

    mail_to = [user_email]
    email_context: dict[str, Any] = {
        "email": user_email,
        "empty_notification_notice": True,
        "enrolled_date": datetime_utils.convert_from_iso_str(
            datetime_utils.get_iso_date()
        ),
        "enrolled_name": full_name,
    }
    schedule(mail_free_trial_start(loaders, mail_to, email_context))


async def update_metadata(
    loaders: Any,
    email: str,
    metadata: EnrollmentMetadataToUpdate,
) -> None:
    if await exists(loaders, email):
        await enrollment_model.update_metadata(
            email=email,
            metadata=metadata,
        )
