from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import logging
from mailer import (
    groups as groups_mail,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


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
        for stakeholder in await loaders.group_stakeholders.load(group):
            if stakeholder["role"] in ["customer_manager", "user_manager"]:
                if users[stakeholder["email"]]:
                    users[stakeholder["email"]].append(group)
                else:
                    users[stakeholder["email"]] = [group]

    if users:
        email_context: dict[str, Any] = {}
        await groups_mail.send_mail_users_weekly_report(
            email_to=[],
            context=email_context,
        )
    else:
        LOGGER.info("- users weekly report NOT sent")
        return


async def main() -> None:
    await send_users_weekly_report()
