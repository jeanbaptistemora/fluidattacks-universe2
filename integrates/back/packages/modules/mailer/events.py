# Standard libraries
from typing import (
    Any,
    List,
)

# Third-party libraries
from aioextensions import collect

# Local libraries
from backend import authz
from backend.typing import (
    Comment as CommentType,
    Event as EventType,
    MailContent as MailContentType,
    Project as GroupType,
)
from group_access import domain as group_access_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PRODUCTION,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
)
from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async_new,
)


async def _get_external_recipients(project: str) -> List[str]:
    recipients = await group_access_domain.get_managers(project)
    return _remove_fluid_from_recipients(recipients)


def _is_not_a_fluidattacks_email(email: str) -> bool:
    return 'fluidattacks.com' not in email


def _remove_fluid_from_recipients(emails: List[str]) -> List[str]:
    new_email_list = list(
        filter(_is_not_a_fluidattacks_email, emails)
    )
    return new_email_list


async def send_mail_comment(  # pylint: disable=too-many-locals
    context: Any,
    comment_data: CommentType,
    user_mail: str,
    event_id: str
) -> None:
    event_loader = context.loaders.event
    event = await event_loader.load(event_id)
    group_name = event['project_name']

    group_loader = context.loaders.group_all
    group = await group_loader.load(group_name)
    org_id = group['organization']

    organization_loader = context.loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    email_context: MailContentType = {
        'comment': comment_data['content'].splitlines(),
        'comment_type': 'event',
        'comment_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
            f'/events/{event_id}/comments'
        ),
        'finding_id': event_id,
        'finding_name': f'Event #{event_id}',
        'parent': str(comment_data['parent']),
        'project': group_name,
        'user_email': user_mail
    }
    recipients = await group_access_domain.get_users_to_notify(
        group_name,
        True
    )
    recipients_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient,
            group_name
        ) in ['customer', 'customeradmin']
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient,
            group_name
        ) not in ['customer', 'customeradmin']
    ]

    email_context_customers = email_context.copy()
    if await authz.get_group_level_role(
        user_mail,
        group_name
    ) not in ['customer', 'customeradmin']:
        email_context_customers['user_email'] = 'Hacker at FluidIntegrates'
    await collect([
        send_mails_async_new(
            mail_recipients,
            mail_context,
            COMMENTS_TAG,
            f'New comment in [{group_name}]',
            'new_comment'
        )
        for mail_recipients, mail_context in zip(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
        )
    ])


async def send_mail_new_event(  # pylint: disable=too-many-arguments
    loaders: Any,
    org_id: str,
    analyst: str,
    event_id: str,
    group_name: str,
    subscription: str,
    event_type: str
) -> None:
    organization_loader = loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    email_context: MailContentType = {
        'analyst_email': analyst,
        'event_id': event_id,
        'event_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/events/{event_id}'
        ),
        'project': group_name,
        'organization': org_name
    }

    recipients = await group_access_domain.list_group_managers(group_name)
    recipients.append(analyst)
    if subscription == 'oneshot':
        recipients.append(FI_MAIL_PROJECTS)
    elif subscription == 'continuous':
        recipients.extend([FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS])
    if event_type in ['CLIENT_APPROVES_CHANGE_TOE']:
        recipients.extend([FI_MAIL_PRODUCTION] + FI_MAIL_REVIEWERS.split(','))

    recipients_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient,
            group_name
        ) == 'customeradmin'
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient,
            group_name
        ) != 'customeradmin'
    ]
    email_context_customers = email_context.copy()
    email_context_customers['analyst_email'] = 'Hacker at FluidIntegrates'

    collect([
        send_mails_async_new(
            mail_recipients,
            mail_context,
            GENERAL_TAG,
            (
                f'New event in [{mail_context["project"]}] - '
                f'[Event#{mail_context["event_id"]}]'
            ),
            'new_event'
        )
        for mail_recipients, mail_context in zip(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
        )
    ])


async def send_mail_unsolved_events(
    context: Any,
    group: GroupType,
    events_data: List[EventType]
) -> None:
    organization_loader = context.organization
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    group_name = group['name']

    recipients = await _get_external_recipients(group_name)
    recipients.append(FI_MAIL_PROJECTS)
    mail_context: MailContentType = {
        'project': group_name.capitalize(),
        'organization': org_name,
        'events_len': int(len(events_data)),
        'event_url': f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/events'
    }
    await send_mails_async_new(
        recipients,
        mail_context,
        GENERAL_TAG,
        f'Unsolved events in [{group_name}]',
        'unsolved_events'
    )
