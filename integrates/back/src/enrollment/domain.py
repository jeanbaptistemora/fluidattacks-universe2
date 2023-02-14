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
    trials as trials_model,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
)
from db_model.trials.types import (
    Trial,
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

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


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

    await trials_model.add(
        trial=Trial(
            completed=False,
            email=user_email,
            extension_date=None,
            extension_days=0,
            start_date=datetime_utils.get_utc_now(),
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
