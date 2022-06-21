from custom_exceptions import (
    EnrollmentNotFound,
    EnrollmentUserExists,
    InvalidParameter,
)
from db_model import (
    enrollment as enrollment_model,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
import logging
import logging.config
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
