from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    get_new_context,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from decorators import (
    retry_on_exceptions,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.groups import (
    send_mail_events_digest,
)
from mailer.utils import (
    get_group_emails_by_notification,
    get_organization_name,
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
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)

mail_events_digest = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(send_mail_events_digest)


class EventsDataType(TypedDict):
    org_name: str
    email_to: tuple[str, ...]
    events: tuple[Event, ...]


def unique_emails(
    events_data: dict[str, EventsDataType],
    email_list: tuple[str, ...],
) -> tuple[str, ...]:
    if events_data:
        email_list += events_data.popitem()[1]["email_to"]
        return unique_emails(events_data, email_list)

    return tuple(set(email_list))


async def send_events_digest() -> None:
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
                notification="events_digest",
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
    for email in unique_emails(dict(groups_data), ()):
        user_content: dict[str, Any] = {
            "groups_data": {
                group_name: {
                    "org_name": data["org_name"],
                    "open_events": data["events"],
                }
                for group_name, data in groups_data.items()
                if email in data["email_to"]
            },
            "date": datetime_utils.get_as_str(
                datetime_utils.get_now_minus_delta(), "%Y-%m-%d"
            ),
        }

        try:
            await mail_events_digest(
                loaders=loaders,
                context=user_content,
                email_to=[],
                email_cc=[],
            )
            LOGGER.info(
                "Events email sent",
                extra={"extra": {"email": email, "data": user_content}},
            )
        except KeyError:
            LOGGER.info(
                "Key error, events email not sent",
                extra={"extra": {"email": email}},
            )
            continue
    LOGGER.info("Events digest report execution finished.")


async def main() -> None:
    await send_events_digest()
