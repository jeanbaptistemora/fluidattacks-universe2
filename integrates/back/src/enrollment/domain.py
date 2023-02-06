from aioextensions import (
    schedule,
)
from custom_exceptions import (
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
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
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
    validate_email_address_deco,
)
from organizations.utils import (
    get_organization,
)
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Optional,
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


@validate_email_address_deco("user_email")
async def add_enrollment(
    *,
    loaders: Dataloaders,
    user_email: str,
    full_name: str,
) -> None:
    if not user_email:
        raise InvalidParameter()

    await companies_model.add(
        company=Company(
            domain=user_email.split("@")[1],
            trial=Trial(
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime_utils.get_utc_now(),
            ),
        )
    )
    await enrollment_model.add(
        enrollment=Enrollment(
            email=user_email,
            enrolled=True,
        )
    )
    await stakeholders_domain.update(
        email=user_email, metadata=StakeholderMetadataToUpdate(enrolled=True)
    )

    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        user_email
    )
    organization = await get_organization(
        loaders, stakeholder_orgs[0].organization_id
    )
    group_names = await group_access_domain.get_stakeholder_groups_names(
        loaders, user_email, True
    )

    schedule(
        mail_free_trial_start(loaders, user_email, full_name, group_names[0])
    )
    # Fallback event
    await analytics.mixpanel_track(
        user_email,
        "AutoenrollSubmit",
        group=group_names[0],
        mp_country_code=organization.country,
        organization=organization.name,
        User=full_name,
    )


async def update_metadata(
    email: str,
    metadata: EnrollmentMetadataToUpdate,
) -> None:
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


async def in_trial(
    loaders: Dataloaders, user_email: str, organization: Organization
) -> bool:
    domain = user_email.split("@")[1]
    company: Optional[Company] = await loaders.company.load(domain)
    completed = company and company.trial.completed

    if completed or organization.payment_methods:
        return False
    return True
