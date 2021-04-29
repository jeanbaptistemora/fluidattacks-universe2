# Standard libraries
from typing import (
    Any,
    cast,
    Dict,
    List,
)

# Third-party libraries
from aioextensions import collect

# Local libraries
from backend import mailer
from backend.api import get_new_context
from backend.typing import (
    Event as EventType,
    Historic as HistoricType,
    MailContent as MailContentType,
)
from events import domain as events_domain
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_PROJECTS,
)
from .common import (
    remove_fluid_from_recipients,
    scheduler_send_mail,
)


async def get_external_recipients(project: str) -> List[str]:
    recipients = await group_access_domain.get_managers(project)
    return remove_fluid_from_recipients(recipients)


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


async def send_unsolved_events_email(context: Any, group_name: str) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    mail_to = []
    events_info_for_email = []
    group_info = await groups_domain.get_attributes(
        group_name, ['historic_configuration']
    )
    historic_configuration = cast(
        HistoricType,
        group_info.get('historic_configuration', [{}])
    )
    if (group_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await get_external_recipients(group_name)
        mail_to.append(FI_MAIL_PROJECTS)
        unsolved_events = await get_unsolved_events(group_name)
        events_info_for_email = [
            extract_info_from_event_dict(x)
            for x in unsolved_events
        ]
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    context_event: MailContentType = {
        'project': group_name.capitalize(),
        'organization': org_name,
        'events_len': int(len(events_info_for_email)),
        'event_url': f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/events'
    }
    if context_event['events_len'] and mail_to:
        scheduler_send_mail(
            mailer.send_mail_unsolved_events,
            mail_to,
            context_event
        )


async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all groups """
    context = get_new_context()
    groups = await groups_domain.get_active_groups()
    await collect(
        send_unsolved_events_email(context, group)
        for group in groups
    )


async def main() -> None:
    await send_unsolved_to_all()
