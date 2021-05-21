
from typing import (
    Any,
    List,
)

from aioextensions import collect

from __init__ import BASE_URL
from custom_types import (
    Comment as CommentType,
    MailContent as MailContentType,
)

from .common import (
    COMMENTS_TAG,
    DIGEST_TAG,
    GENERAL_TAG,
    get_email_recipients,
    send_mails_async_new,
)


async def send_mail_access_granted(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'Access Granted to group {context["project"]} '
            'in Integrates by Fluid Attacks'
        ),
        'access_granted'
    )


async def send_mail_daily_digest(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        DIGEST_TAG,
        f'Daily Digest for [{context["project"]}]',
        'daily_digest'
    )


async def send_mail_group_report(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'{context["filetype"]} report for [{context["projectname"]}]',
        'project_report'
    )


async def send_mail_comment(  # pylint: disable=too-many-locals
    context: Any,
    comment_data: CommentType,
    user_mail: str,
    group_name: str = ''
) -> None:
    group_loader = context.loaders.group_all
    group = await group_loader.load(group_name)
    org_id = group['organization']

    organization_loader = context.loaders.organization
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    email_context: MailContentType = {
        'comment': comment_data['content'].splitlines(),
        'comment_type': 'project',
        'comment_url': (
            f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/consulting'
        ),
        'parent': str(comment_data['parent']),
        'project': group_name,
        'user_email': user_mail,
    }
    # Mask Fluid Attacks' staff
    recipients = await get_email_recipients(group_name, True)
    recipients_not_masked = [
        recipient
        for recipient in recipients
        if (
            '@fluidattacks.com' in recipient or
            '@fluidattacks.com' not in user_mail
        )
    ]
    recipients_masked = [
        recipient
        for recipient in recipients
        if (
            '@fluidattacks.com' not in recipient and
            '@fluidattacks.com' in user_mail
        )
    ]
    email_context_masked = email_context.copy()
    if '@fluidattacks.com' in user_mail:
        email_context_masked['user_email'] = 'Hacker at Fluid Attacks'
    await collect([
        send_mails_async_new(
            mail_recipients,
            mail_context,
            COMMENTS_TAG,
            f'New comment in [{group_name}]',
            'new_comment'
        )
        for mail_recipients, mail_context in zip(
            [recipients_not_masked, recipients_masked],
            [email_context, email_context_masked]
        )
    ])
