# Standard libraries
import logging
import logging.config
from typing import (
    cast,
    Dict,
    List,
)

# Third-party libraries
from aioextensions import collect

# Local libraries
from back.settings import LOGGING
from backend.typing import MailContent as MailContentType
from dataloaders import get_new_context
from findings import domain as findings_domain
from groups import domain as groups_domain
from mailer import findings as findings_mail
from __init__ import (
    BASE_URL,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
)
from .common import scheduler_send_mail


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    active_projects = await groups_domain.get_active_groups()
    findings = []
    pending_verification_findings = await collect(
        findings_domain.get_pending_verification_findings(
            get_new_context(),
            project
        )
        for project in active_projects
    )
    for project_findings in pending_verification_findings:
        findings += project_findings

    if findings:
        try:
            mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
            context: MailContentType = {'findings': list(), 'total': 0}
            for finding in findings:
                cast(
                    List[Dict[str, str]],
                    context['findings']
                ).append({
                    'finding_name': finding['finding'],
                    'finding_url': (
                        f'{BASE_URL}/groups/'
                        f'{str.lower(str(finding["project_name"]))}/'
                        f'{finding["finding_id"]}/description'
                    ),
                    'project': str.upper(str(finding['project_name']))
                })
            context['total'] = len(findings)
            scheduler_send_mail(
                findings_mail.send_mail_new_remediated,
                mail_to,
                context
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={'extra': locals()})


async def main() -> None:
    await get_remediated_findings()
