from aioextensions import (
    collect,
)
from companies import (
    domain as companies_domain,
)
from custom_exceptions import (
    InvalidManagedChange,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.companies.types import (
    Company,
    CompanyMetadataToUpdate,
    Trial,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from groups import (
    domain as groups_domain,
)
import logging
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
FREE_TRIAL_DAYS = 21
LOGGER = logging.getLogger(__name__)


async def _expire(
    loaders: Dataloaders,
    group: Group,
    company: Company,
) -> None:
    try:
        LOGGER.info(
            "Will expire group %s, created_by %s, start_date %s",
            group.name,
            group.created_by,
            company.trial.start_date,
        )
        await companies_domain.update_metadata(
            domain=company.domain,
            metadata=CompanyMetadataToUpdate(
                trial=company.trial._replace(completed=True)
            ),
        )
        await groups_domain.update_group_managed(
            loaders=loaders,
            comments="Trial period has expired",
            email="integrates@fluidattacks.com",
            group_name=group.name,
            managed=GroupManaged.UNDER_REVIEW,
        )
        await groups_mail.send_mail_free_trial_over(
            loaders=loaders,
            email_to=[group.created_by],
            group_name=group.name,
        )
    except InvalidManagedChange:
        LOGGER.exception(
            "Couldn't expire group %s, managed %s",
            group.name,
            group.state.managed,
        )


def _get_days_since(date: datetime) -> int:
    return (datetime_utils.get_utc_now() - date).days


def _get_remaining_days(trial: Trial) -> int:
    days: int = 0
    if trial.extension_date:
        days = trial.extension_days - _get_days_since(trial.extension_date)
    elif trial.start_date:
        days = FREE_TRIAL_DAYS - _get_days_since(trial.start_date)

    return max(0, days)


def _has_expired(trial: Trial) -> bool:
    return (
        not trial.completed
        and trial.start_date is not None
        and _get_remaining_days(trial) == 0
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    domains = tuple(group.created_by.split("@")[1] for group in groups)
    companies: tuple[Optional[Company], ...] = await loaders.company.load_many(
        domains
    )

    await collect(
        tuple(
            _expire(loaders, group, company)
            for group, company in zip(groups, companies)
            if company and _has_expired(company.trial)
        )
    )
