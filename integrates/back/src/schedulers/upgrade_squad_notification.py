from aioextensions import (
    collect,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    get_new_context,
)
from db_model.companies.types import (
    Company,
)
from db_model.groups.enums import (
    GroupManaged,
)
from decorators import (
    retry_on_exceptions,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Optional,
)

# Constants
TRIAL_DAYS = 17


mail_upgrade_squad_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_upgrade_squad_notification)


async def send_upgrade_squad_notification() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    domains = tuple(group.created_by.split("@")[1] for group in groups)
    companies: tuple[Optional[Company], ...] = await loaders.company.load_many(
        domains
    )

    await collect(
        tuple(
            mail_upgrade_squad_notification(loaders, group.created_by)
            for group, company in zip(groups, companies)
            if group.state.managed == GroupManaged.TRIAL
            and company
            and company.trial.start_date
            and datetime_utils.get_days_since(company.trial.start_date)
            == TRIAL_DAYS
        )
    )


async def main() -> None:
    await send_upgrade_squad_notification()
