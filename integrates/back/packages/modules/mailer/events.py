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
    MailContent as MailContentType,
)
from group_access import domain as group_access_domain
from __init__ import BASE_URL
from .common import (
    COMMENTS_TAG,
    GENERAL_TAG,
    send_mails_async_new,
)


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


async def send_mail_new_event(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'New event in [{context["project"]}] - '
            f'[Event#{context["event_id"]}]'
        ),
        'new_event'
    )


async def send_mail_unsolved_events(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Unsolved events in [{context["project"]}]',
        'unsolved_events'
    )
