
from typing import (
    Any,
    Dict,
    List,
    cast,
)

from aioextensions import (
    collect,
    schedule,
)

from custom_types import Event as EventType
from dataloaders import get_new_context
from events import domain as events_domain
from groups import domain as groups_domain
from mailer import events as events_mail


async def get_unsolved_events(project: str) -> List[EventType]:
    events = await events_domain.list_group_events(project)
    event_list = await collect(
        events_domain.get_event(event)
        for event in events
    )
    unsolved_events = list(filter(is_an_unsolved_event, event_list))
    return unsolved_events


def extract_info_from_event_dict(event_dict: EventType) -> EventType:
    event_dict = {
        'type': event_dict.get('event_type', ''),
        'details': event_dict.get('detail', '')
    }
    return event_dict


def is_an_unsolved_event(event: EventType) -> bool:
    return cast(
        List[Dict[str, str]],
        event.get('historic_state', [{}])
    )[-1].get('state', '') == 'CREATED'


async def send_unsolved_events(context: Any, group_name: str) -> None:
    group_loader = context.group_all
    group = await group_loader.load(group_name)

    events_info_for_email = []
    if group['subscription'] == 'continuous':
        unsolved_events = await get_unsolved_events(group_name)
        events_info_for_email = [
            extract_info_from_event_dict(x)
            for x in unsolved_events
        ]
    if events_info_for_email:
        schedule(
            events_mail.send_mail_unsolved_events(
                context,
                group,
                events_info_for_email
            )
        )


async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all groups """
    context = get_new_context()
    groups = await groups_domain.get_active_groups()
    await collect([
        send_unsolved_events(context, group)
        for group in groups
    ])


async def main() -> None:
    await send_unsolved_to_all()
