from aioextensions import (
    collect,
)
from custom_exceptions import (
    InvalidManagedChange,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enrollment.types import (
    Enrollment,
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
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
FREE_TRIAL_DAYS = 21


def get_days_since(date: str) -> int:
    return (
        datetime_utils.get_now()
        - datetime_utils.get_datetime_from_iso_str(date)
    ).days


async def expire(loaders: Dataloaders, group: Group) -> None:
    try:
        LOGGER.info("Will expire %s", group.name)
        await groups_domain.update_group_managed(
            loaders=loaders,
            comments="Trial period has expired",
            group_name=group.name,
            managed=GroupManaged.UNDER_REVIEW,
            user_email="integrates@fluidattacks.com",
        )
    except InvalidManagedChange:
        LOGGER.exception("Couldn't expire %s", group.name)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    group_authors = tuple(group.created_by for group in groups)
    enrollments: tuple[Enrollment, ...] = loaders.enrollment.load_many(
        group_authors
    )

    await collect(
        tuple(
            expire(loaders, group)
            for group, enrollment in zip(groups, enrollments)
            if not enrollment.trial.completed
            and get_days_since(enrollment.trial.start_date)
            - enrollment.trial.extension_days
            >= FREE_TRIAL_DAYS
        )
    )
