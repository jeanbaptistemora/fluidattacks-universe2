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
from db_model.stakeholders.types import (
    Stakeholder,
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
INACTIVE_DAYS = 21


async def send_reminder_notification() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group_name
            for group_name in group_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        )

    groups = await loaders.group.load_many(group_names)
    orgs_ids: set[str] = set(group.organization_id for group in groups)

    stakeholders_emails: list[str] = [
        stakeholder.email
        for org_id in orgs_ids
        for stakeholder in await loaders.organization_stakeholders.load(org_id)
        if (
            stakeholder.last_login_date
            and (
                datetime_utils.get_now()
                - datetime_utils.get_datetime_from_iso_str(
                    stakeholder.last_login_date
                )
            ).days
            == INACTIVE_DAYS
            and await orgs_domain.get_stakeholder_role(
                email=stakeholder.email,
                is_registered=stakeholder.is_registered,
                organization_id=org_id,
            )
            in ["customer_manager", "user_manager"]
        )
    ]

    stakeholders_emails_filtered: list[str] = [
        key for key, _ in groupby(sorted(stakeholders_emails))
    ]

    stakeholders: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(stakeholders_emails_filtered)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders
        if Notification.REMINDER_NOTIFICATION
        in stakeholder.notifications_preferences.email
    ]

    if stakeholders_email:
        await groups_mail.send_mail_reminder(
            loaders=loaders,
            context={},
            email_to=stakeholders_email,
        )
    else:
        LOGGER.info("- reminder notification NOT sent")
        return


async def main() -> None:
    await send_reminder_notification()
