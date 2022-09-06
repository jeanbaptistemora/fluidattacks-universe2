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
    EnrollmentMetadataToUpdate,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from enrollment import (
    domain as enrollment_domain,
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

logging.config.dictConfig(LOGGING)

# Constants
FREE_TRIAL_DAYS = 21
LOGGER = logging.getLogger(__name__)


def get_days_since(date: str) -> int:
    return (
        datetime_utils.get_now()
        - datetime_utils.get_datetime_from_iso_str(date)
    ).days


async def expire(
    loaders: Dataloaders,
    group: Group,
    enrollment: Enrollment,
) -> None:
    try:
        LOGGER.info("Will expire %s", group.name)
        await enrollment_domain.update_metadata(
            loaders=loaders,
            email=group.created_by,
            metadata=EnrollmentMetadataToUpdate(
                trial=enrollment.trial._replace(completed=True)
            ),
        )
        await groups_domain.update_group_managed(
            loaders=loaders,
            comments="Trial period has expired",
            group_name=group.name,
            managed=GroupManaged.UNDER_REVIEW,
            user_email="integrates@fluidattacks.com",
        )
        await groups_mail.send_mail_free_trial_over(
            loaders=loaders,
            email_to=[group.created_by],
            group_name=group.name,
        )
    except InvalidManagedChange:
        LOGGER.exception("Couldn't expire %s", group.name)


def get_remaining_days(enrollment: Enrollment) -> int:
    trial = enrollment.trial
    days = (
        trial.extension_days - get_days_since(trial.extension_date)
        if trial.extension_date
        else FREE_TRIAL_DAYS - get_days_since(trial.start_date)
    )

    return max(0, days)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    group_authors = tuple(group.created_by for group in groups)
    enrollments: tuple[Enrollment, ...] = loaders.enrollment.load_many(
        group_authors
    )

    await collect(
        tuple(
            expire(loaders, group, enrollment)
            for group, enrollment in zip(groups, enrollments)
            if not enrollment.trial.completed
            and enrollment.trial.start_date
            and get_remaining_days(enrollment) == 0
        )
    )
