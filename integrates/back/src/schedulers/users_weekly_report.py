from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
    Any,
    Dict,
    List,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
INACTIVE_DAYS = 7


def get_inactive_users(
    group_stakeholders: Tuple[Dict[str, Any], ...],
) -> List[str]:
    inactive_users: list[str] = [
        stakeholder["email"]
        for stakeholder in group_stakeholders
        if (
            stakeholder["last_login"]
            and (
                datetime_utils.get_now()
                - datetime_utils.get_datetime_from_iso_str(
                    stakeholder["last_login"]
                )
            ).days
            >= INACTIVE_DAYS
        )
    ]
    return inactive_users


async def send_users_weekly_report() -> None:
    loaders: Dataloaders = get_new_context()

    group_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group_name
            for group_name in group_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        )

    users: dict[str, list[str]] = {}

    for group in group_names:
        group_stakeholders: tuple[
            Stakeholder, ...
        ] = await loaders.group_stakeholders.load(group)
        for stakeholder in group_stakeholders:
            if stakeholder.role in ["customer_manager", "user_manager"]:
                if users[stakeholder.email]:
                    users[stakeholder.email].append(group)
                else:
                    users[stakeholder.email] = [group]

    if users:
        email_context: dict[str, Any] = {}
        await groups_mail.send_mail_users_weekly_report(
            loaders=loaders,
            email_to=[],
            context=email_context,
        )
    else:
        LOGGER.info("- users weekly report NOT sent")
        return


async def main() -> None:
    await send_users_weekly_report()
