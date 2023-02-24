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
    Event,
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
from typing import (
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


class EventsDataType(TypedDict):
    org_name: str
    email_to: tuple[str, ...]
    events: tuple[Event, ...]


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
    groups_data: dict[str, EventsDataType] = dict(
        zip(
            groups_names,
            [
                {
                    "org_name": org_name,
                    "email_to": tuple(email_to),
                    "events": tuple(event),
                }
                for org_name, email_to, event in zip(
                    groups_org_names, groups_stakeholders_email, groups_events
                )
            ],
        )
    )
    groups_data = {
        group_name: data
        for (group_name, data) in groups_data.items()
        if (data["email_to"] and (data["events"]))
    }
    LOGGER.info(
        "Events by have been obtained",
        extra={
            "extra": {
                "groups_data": groups_data,
            }
        },
    )


async def main() -> None:
    await send_event_digest()
