from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
)
from db_model.groups.enums import (
    GroupService,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.roots.types import (
    Root,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access import (
    domain as group_access_domain,
)
from groups.domain import (
    get_creation_date,
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
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def has_environment(
    loaders: Dataloaders,
    group: str,
) -> bool:
    roots: Tuple[Root, ...] = await loaders.group_roots.load(group)
    git_roots = await loaders.git_environment_urls.load_many_chained(
        [root.id for root in roots]
    )
    return any(git_roots)


async def _send_mail_report(
    loaders: Dataloaders,
    group: str,
    group_date_delta: int,
) -> None:
    group_stakeholders: Tuple[
        Stakeholder, ...
    ] = await group_access_domain.get_group_stakeholders(loaders, group)

    stakeholders_emails = [
        stakeholder.email
        for stakeholder in group_stakeholders
        if await group_access_domain.get_stakeholder_role(
            loaders, stakeholder.email, group, stakeholder.is_registered
        )
        in ["customer_manager", "user_manager", "vulnerability_manager"]
    ]
    context: Dict[str, Any] = {
        "group": group,
        "group_date": group_date_delta,
    }
    await groups_mail.send_mail_missing_environment_alert(
        loaders=loaders,
        context=context,
        email_to=stakeholders_emails,
    )


async def missing_environment_alert() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    group_names = tuple(
        group.name
        for group in active_groups
        if (
            group.state.has_machine
            and group.state.tier != GroupTier.ONESHOT
            and not (
                group.state.type == GroupSubscriptionType.CONTINUOUS
                and group.state.service == GroupService.BLACK
            )
        )
    )

    if FI_ENVIRONMENT == "production":
        group_names = tuple(
            group
            for group in group_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    if group_names:
        for group in group_names:
            creation_date: date = datetime_utils.get_date_from_iso_str(
                await get_creation_date(loaders, group)
            )
            group_date_delta: int = (
                datetime_utils.get_now().date() - creation_date
            ).days
            has_env: bool = await has_environment(loaders, group)
            if (
                not has_env
                and group_date_delta > 0
                and (group_date_delta % 30 == 0 or group_date_delta == 7)
            ):
                await _send_mail_report(
                    loaders, group, (group_date_delta // 7)
                )
    else:
        LOGGER.info("- environment alert NOT sent")
        return


async def main() -> None:
    await missing_environment_alert()
