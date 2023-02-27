from aioextensions import (
    collect,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
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
    events_comments: dict[str, tuple[EventComment, ...]]


def filter_last_event_comments(
    comments: Iterable[EventComment],
) -> list[EventComment]:
    return [
        comment
        for comment in comments
        if is_last_day_comment(comment.creation_date)
    ]


def get_days_since_comment(date: datetime) -> int:
    return (datetime_utils.get_utc_now() - date).days


async def group_event_comments(
    loaders: Dataloaders,
    groups_events: Iterable[Event],
) -> dict[str, tuple[EventComment, ...]]:
    comments = await collect(
        [
            events_comments(loaders, event.id)
            for event in groups_events
            if event.id
        ]
    )

    events_dic = dict(
        zip(
            [event.id for event in groups_events],
            comments,
        )
    )

    return {
        event_id: event_comment
        for event_id, event_comment in events_dic.items()
        if event_comment
    }


async def events_comments(
    loaders: Dataloaders, instance_id: str
) -> tuple[EventComment, ...]:
    return tuple(
        filter_last_event_comments(
            await loaders.event_comments.load(instance_id)
        )
    )


def is_last_day_comment(creation_date: datetime) -> bool:
    comments_age = 3 if datetime_utils.get_now().weekday() == 0 else 1

    return get_days_since_comment(creation_date) < comments_age


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
    groups_events_comments = await collect(
        [
            group_event_comments(loaders, group_events)
            for group_events in groups_events
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
                    "events_comments": event_comments,
                }
                for org_name, email_to, event, event_comments in zip(
                    groups_org_names,
                    groups_stakeholders_email,
                    groups_events,
                    groups_events_comments,
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
                    "events_comments": data["events_comments"],
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


def unique_emails(
    events_data: dict[str, EventsDataType],
    email_list: tuple[str, ...],
) -> tuple[str, ...]:
    if events_data:
        email_list += events_data.popitem()[1]["email_to"]
        return unique_emails(events_data, email_list)

    return tuple(set(email_list))


async def main() -> None:
    await send_events_digest()
