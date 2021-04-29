# Standard libraries
from typing import (
    Any,
    Dict,
    List,
)

# Third-party libraries
from aioextensions import in_process

# Local libraries
from backend.typing import MailContent as MailContentType
from group_access import domain as group_access_domain
from newutils import vulnerabilities as vulns_utils
from __init__ import BASE_URL
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


async def send_mail_new_releases(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'Findings to release ({context["total_unreleased"]})'
            f'({context["total_unsubmitted"]})'
        ),
        'new_releases'
    )


async def send_mail_new_remediated(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'Findings to verify ({context["total"]}) '
            f'in [{context["project"]}]'
        ),
        'new_remediated'
    )


async def send_mail_reject_draft(
    email_to: List[str],
    context: MailContentType
) -> None:
    await send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        (
            f'Draft unsubmitted in [{context["project"]}] - '
            f'#{context["finding_id"]}'
        ),
        'unsubmitted_draft'
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


async def send_mail_verified_finding(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    finding_name: str,
    group_name: str,
    historic_verification: List[Dict[str, str]],
    vulnerabilities: List[str]
) -> None:
    group_loader = context.group_all
    group = await group_loader.load(group_name)

    organization_loader = context.organization
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']

    all_recipients = await group_access_domain.get_users_to_notify(group_name)
    recipients = await in_process(
        vulns_utils.get_reattack_requesters,
        historic_verification,
        vulnerabilities
    )
    recipients = [
        recipient
        for recipient in recipients
        if recipient in all_recipients
    ]
    await send_mails_async_new(
        recipients,
        {
            'project': group_name,
            'organization': org_name,
            'finding_name': finding_name,
            'finding_url': (
                f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                f'/vulns/{finding_id}/tracking'
            ),
            'finding_id': finding_id
        },
        VERIFY_TAG,
        (
            f'Finding verified in [{context["project"]}] - '
            f'[Finding#{context["finding_id"]}]'
        ),
        'verified_finding'
    )
