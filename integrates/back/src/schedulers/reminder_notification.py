from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Notification,
)
from db_model.users.types import (
    User,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    groupby,
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
    List,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
INACTIVE_DAYS = 21


async def send_reminder_notification() -> None:
    group_names = await groups_domain.get_active_groups()
    loaders: Dataloaders = get_new_context()

    if FI_ENVIRONMENT == "production":
        group_names = [
            group_name
            for group_name in group_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        ]

    groups = await loaders.group_typed.load_many(group_names)
    orgs_ids: set = set(
        await collect(
            orgs_domain.get_id_by_name(group.organization_name)
            for group in groups
        )
    )

    stakeholders_emails: List[str] = [
        stakeholder["email"]
        for org_id in orgs_ids
        for stakeholder in await loaders.organization_stakeholders.load(org_id)
        if (
            stakeholder["last_login"]
            and (
                datetime_utils.get_now()
                - datetime_utils.get_datetime_from_iso_str(
                    stakeholder["last_login"]
                )
            ).days
            == INACTIVE_DAYS
            and stakeholder["role"] in ["customer_manager", "user_manager"]
        )
    ]

    stakeholders_emails_filtered: List[str] = [
        key for key, group in groupby(sorted(stakeholders_emails))
    ]

    users: Tuple[User, ...] = await loaders.user.load_many(
        stakeholders_emails_filtered
    )
    users_email = [
        user.email
        for user in users
        if Notification.NEW_COMMENT in user.notifications_preferences.email
    ]

    if users_email:
        await groups_mail.send_mail_reminder(
            context={},
            email_to=users_email,
        )
    else:
        LOGGER.info("- reminder notification NOT sent")
        return


async def main() -> None:
    await send_reminder_notification()
