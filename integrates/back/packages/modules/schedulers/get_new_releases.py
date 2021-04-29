# Standard libraries
import logging
import logging.config
from collections import defaultdict
from typing import (
    cast,
    Dict,
    List,
)

# Third-party libraries
from aioextensions import collect

# Local libraries
from back.settings import LOGGING
from backend.api import get_new_context
from backend.typing import MailContent as MailContentType
from findings import domain as findings_domain
from groups import domain as groups_domain
from mailer import findings as findings_mail
from newutils import findings as findings_utils
from __init__ import (
    BASE_URL,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
    FI_TEST_PROJECTS,
)
from .common import scheduler_send_mail


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_new_releases() -> None:  # pylint: disable=too-many-locals
    """Summary mail send with findings that have not been released yet."""
    context = get_new_context()
    group_loader = context.group_all
    organization_loader = context.organization
    test_groups = FI_TEST_PROJECTS.split(',')
    groups = await groups_domain.get_active_groups()
    email_context: MailContentType = defaultdict(list)
    cont = 0
    groups = [
        group
        for group in groups
        if group not in test_groups
    ]
    list_drafts = await findings_domain.list_drafts(groups)
    group_drafts = await collect(
        findings_domain.get_findings_async(drafts)
        for drafts in list_drafts
    )
    for group_name, finding_requests in zip(groups, group_drafts):
        if group_name not in test_groups:
            try:
                for finding in finding_requests:
                    is_finding_released = findings_utils.is_released(finding)
                    if not is_finding_released:
                        group = await group_loader.load(group_name)
                        org_id = group['organization']
                        organization = await organization_loader.load(org_id)
                        org_name = organization['name']
                        submission = finding.get('historicState')
                        status = submission[-1].get('state')
                        category = (
                            'unsubmitted'
                            if status in ('CREATED', 'REJECTED')
                            else 'unreleased'
                        )
                        cast(
                            List[Dict[str, str]],
                            email_context[category]
                        ).append({
                            'finding_name': finding.get('finding'),
                            'finding_url': (
                                f'{BASE_URL}/orgs/{org_name}/groups/'
                                f'{group_name}/drafts/'
                                f'{finding.get("findingId")}/description'
                            ),
                            'project': group_name.upper(),
                            'organization': org_name
                        })
                        cont += 1
            except (TypeError, KeyError) as ex:
                LOGGER.exception(ex, extra={'extra': locals()})
        else:
            # ignore test projects
            pass
    if cont > 0:
        email_context['total_unreleased'] = len(
            cast(List[Dict[str, str]], email_context['unreleased'])
        )
        email_context['total_unsubmitted'] = len(
            cast(List[Dict[str, str]], email_context['unsubmitted'])
        )
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        scheduler_send_mail(
            findings_mail.send_mail_new_releases,
            mail_to,
            email_context
        )


async def main() -> None:
    await get_new_releases()
