# Standard libraries
from typing import List

# Third-party libraries

# Local libraries
from backend.typing import MailContent as MailContentType
from .common import (
    GENERAL_TAG,
    VERIFY_TAG,
    send_mails_async_new,
)


async def send_mail_delete_finding(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'Finding #{context["finding_id"]} in [{context["project"]}] '
            'was removed'
        ),
        'delete_finding'
    )


async def send_mail_new_draft(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'New draft submitted in [{context["project"]}] - '
            f'[Finding#{context["finding_id"]}]'
        ),
        'new_draft'
    )


async def send_mail_remediate_finding(
    email_to: List[str],
    context: MailContentType
) -> None:
    context['solution_description'] = (
        f'"{context["solution_description"]}"'.splitlines()
    )
    await send_mails_async_new(
        email_to,
        context,
        VERIFY_TAG,
        (
            f'New remediation in [{context["project"]}] - ' +
            f'[Finding#{context["finding_id"]}]'
        ),
        'remediate_finding'
    )
