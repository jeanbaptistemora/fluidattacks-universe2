from aioextensions import (
    collect,
    schedule,
)
from custom_exceptions import (
    EnrollmentNotFound,
    EnrollmentUserExists,
    InvalidParameter,
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    companies as companies_model,
    enrollment as enrollment_model,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.enrollment.enums import (
    EnrollmentTrialState,
)
from db_model.enrollment.types import (
    Enrollment,
    EnrollmentMetadataToUpdate,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
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
    analytics,
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_email_address,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
TRIAL_PERIOD_DAYS: int = 21
EXTENDED_TRIAL_PERIOD_DAYS: int = 9


mail_free_trial_start = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_free_trial_start)


async def exists(
    loaders: Dataloaders,
    user_email: str,
) -> bool:
    try:
        enrollment: Enrollment = await loaders.enrollment.load(user_email)
        return enrollment.enrolled
    except EnrollmentNotFound:
        return False


async def add_enrollment(
    *,
    loaders: Dataloaders,
    user_email: str,
    full_name: str,
) -> None:
    validate_email_address(user_email)

    if not user_email:
        raise InvalidParameter()

    if await exists(loaders, user_email):
        raise EnrollmentUserExists.new()

    await collect(
        [
            companies_model.add(
                company=Company(
                    domain=user_email.split("@")[1],
                    trial=Trial(
                        completed=False,
                        extension_date=None,
                        extension_days=0,
                        start_date=datetime_utils.get_utc_now(),
                    ),
                )
            ),
            enrollment_model.add(
                enrollment=Enrollment(
                    email=user_email,
                    enrolled=True,
                )
            ),
        ]
    )

    group_names = await group_access_domain.get_stakeholder_groups_names(
        loaders, user_email, True
    )

    schedule(
        mail_free_trial_start(loaders, user_email, full_name, group_names[0])
    )
    await analytics.mixpanel_track(
        user_email,
        "AutoenrollSubmit",
        group=group_names[0],
    )


async def update_metadata(
    loaders: Dataloaders,
    email: str,
    metadata: EnrollmentMetadataToUpdate,
) -> None:
    if await exists(loaders, email):
        await enrollment_model.update_metadata(
            email=email,
            metadata=metadata,
        )


def get_enrollment_trial_state(trial: Trial) -> EnrollmentTrialState:
    if not trial.start_date:
        return EnrollmentTrialState.TRIAL_ENDED

    if (
        datetime_utils.get_plus_delta(
            trial.start_date,
            days=TRIAL_PERIOD_DAYS,
        )
        > datetime_utils.get_utc_now()
    ):
        return EnrollmentTrialState.TRIAL

    if not trial.extension_days or not trial.extension_date:
        return EnrollmentTrialState.TRIAL_ENDED

    if (
        datetime_utils.get_plus_delta(
            trial.extension_date,
            days=EXTENDED_TRIAL_PERIOD_DAYS,
        )
        > datetime_utils.get_utc_now()
    ):
        return EnrollmentTrialState.EXTENDED

    return EnrollmentTrialState.EXTENDED_ENDED


async def is_trial(
    loaders: Dataloaders, user_email: str, organization: Organization
) -> bool:
    domain = user_email.split("@")[1]
    company: Company = await loaders.company.load(domain)
    in_trial = company and not company.trial.completed

    if not in_trial or organization.payment_methods:
        return False
    return True
