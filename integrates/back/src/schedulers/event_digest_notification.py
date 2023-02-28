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
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    EventState,
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
    Union,
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
    event_comments: dict[str, tuple[EventComment, ...]]
    event_states: dict[str, tuple[EventState, ...]]
    open_events: list[dict[str, Union[datetime, str]]]


def filter_last_instances(
    instances: Iterable[Union[EventComment, EventState]],
) -> list[Any]:
    return [
        instance
        for instance in instances
        if is_last_day_instance(
            instance.creation_date
            if isinstance(instance, EventComment)
            else instance.modified_date
        )
    ]


def get_days_since(date: datetime) -> int:
    return (datetime_utils.get_utc_now() - date).days


async def get_event_comments(
    loaders: Dataloaders, event_id: str
) -> tuple[EventComment, ...]:
    return tuple(
        filter_last_instances(await loaders.event_comments.load(event_id))
    )


async def get_event_states(
    loaders: Dataloaders, event_id: str
) -> tuple[EventState, ...]:
    return tuple(
        filter_last_instances(
            await loaders.event_historic_state.load(event_id)
        )
    )


async def get_group_event_comments(
    loaders: Dataloaders,
    groups_events: Iterable[Event],
) -> dict[str, tuple[EventComment, ...]]:
    comments = await collect(
        [
            get_event_comments(loaders, event.id)
            for event in groups_events
            if event.id
        ]
    )

    events_comments = dict(
        zip(
            [event.id for event in groups_events],
            comments,
        )
    )

    return {
        event_id: event_comment
        for event_id, event_comment in events_comments.items()
        if event_comment
    }


async def get_group_event_states(
    loaders: Dataloaders,
    groups_events: Iterable[Event],
) -> dict[str, tuple[EventState, ...]]:
    states = await collect(
        [
            get_event_states(loaders, event.id)
            for event in groups_events
            if event.id
        ]
    )

    events_states = dict(
        zip(
            [event.id for event in groups_events],
            states,
        )
    )

    return {
        event_id: event_states
        for event_id, event_states in events_states.items()
        if event_states
    }


def get_open_events(
    events: list[Event],
) -> list[dict[str, Union[datetime, str]]]:
    return [
        dict(
            created_date=event.created_date,
            description=event.description,
            id=event.id,
        )
        for event in events
        if event.state.status
        in [EventStateStatus.CREATED, EventStateStatus.VERIFICATION_REQUESTED]
    ]


def is_last_day_instance(creation_date: datetime) -> bool:
    instance_age = 3 if datetime_utils.get_now().weekday() == 0 else 1

    return get_days_since(creation_date) < instance_age


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
    groups_open_events = [
        get_open_events(group_events) for group_events in groups_events
    ]
    groups_events_comments = await collect(
        [
            get_group_event_comments(loaders, group_events)
            for group_events in groups_events
        ]
    )
    groups_events_states = await collect(
        [
            get_group_event_states(loaders, group_events)
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
                    "event_comments": event_comments,
                    "event_states": event_states,
                    "open_events": open_events,
                }
                for (
                    org_name,
                    email_to,
                    event,
                    event_comments,
                    event_states,
                    open_events,
                ) in zip(
                    groups_org_names,
                    groups_stakeholders_email,
                    groups_events,
                    groups_events_comments,
                    groups_events_states,
                    groups_open_events,
                )
            ],
        )
    )
    groups_data = {
        group_name: data
        for (group_name, data) in groups_data.items()
        if (
            data["email_to"]
            and (
                data["events"]
                or data["event_comments"]
                or data["event_states"]
                or data["open_events"]
            )
        )
    }
    for email in unique_emails(dict(groups_data), ()):
        user_content: dict[str, Any] = {
            "groups_data": {
                group_name: {
                    "org_name": data["org_name"],
                    "events": data["events"],
                    "event_comments": data["event_comments"],
                    "event_states": data["event_states"],
                    "open_events": data["open_events"],
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
