from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    get_new_context,
)
from db_model.events.types import (
    GroupEventsRequest,
)
import logging
import logging.config
from mailer.utils import (
    get_group_emails_by_notification,
    get_organization_name,
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


async def send_event_digest() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)

    if FI_ENVIRONMENT == "production":
        groups = tuple(
            group
            for group in groups
            if group.name not in FI_TEST_PROJECTS.split(",")
            and group.state.has_squad
        )

    groups_names = tuple(group.name for group in groups)
    groups_org_names = await collect(
        [
            get_organization_name(loaders, group_name)
            for group_name in groups_names
        ]
    )
    groups_stakeholders_email: tuple[list[str], ...] = await collect(
        [
            get_group_emails_by_notification(
                loaders=loaders,
                group_name=group_name,
                notification="consulting_digest",
            )
            for group_name in groups_names
        ]
    )
    groups_events = await loaders.group_events.load_many(
        [
            GroupEventsRequest(group_name=group_name)
            for group_name in groups_names
        ]
    )
    LOGGER.info(
        "Groups events have been obtained",
        extra={
            "extra": {
                "groups_events": groups_events,
                "groups_org_names": groups_org_names,
                "groups_stakeholders_email": groups_stakeholders_email,
            }
        },
    )


async def main() -> None:
    await send_event_digest()
