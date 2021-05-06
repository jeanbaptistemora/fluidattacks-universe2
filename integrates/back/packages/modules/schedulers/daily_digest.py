# Standard libraries
import logging
import logging.config
from operator import itemgetter
from typing import (
    Any,
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    schedule,
)

# Local libraries
from backend.api import get_new_context
from backend.typing import (
    Finding as FindingType,
    MailContent as MailContentType,
)
from findings import domain as findings_domain
from group_comments.domain import get_total_comments_date
from groups.domain import (
    get_mean_remediate,
    get_remediation_rate,
)
from mailer import groups as groups_mail
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from __init__ import (
    FI_MAIL_DIGEST,
    FI_TEST_PROJECTS_DIGEST,
)


bugsnag_utils.start_scheduler_session()

LOGGER = logging.getLogger(__name__)


async def get_oldest_open_findings(
    context: Any,
    findings: List[Dict[str, FindingType]],
    count: int,
) -> list:
    """Get the n oldest open findings and their age"""
    finding_vulns_loader = context.finding_vulns_nzr
    open_findings = [
        finding
        for finding in findings
        if len(vulns_utils.filter_open_vulns(
            await finding_vulns_loader.load(finding['finding_id'])))
    ]
    findings_age = [
        {
            'finding_name': finding['finding'],
            'finding_age': await findings_domain.get_finding_open_age(
                context,
                finding['finding_id'],
            ),
        }
        for finding in open_findings
    ]
    oldest = sorted(
        findings_age,
        key=itemgetter('finding_age'),
        reverse=True
    )[:count]
    return oldest


async def get_group_digest_stats(
    context: Any,
    group_name: str
) -> MailContentType:
    mail_context: MailContentType = {
        'project': group_name,
        'remediation_rate': 0,
        'reattack_effectiveness': 0,
        'remediation_time': 0,
        'queries': 0,
        'reattacks': {
            'reattacks_requested': 0,
            'reattacks_executed': 0,
            'pending_attacks': 0,
        },
        'treatments': {
            'temporary_applied': 0,
            'eternal_requested': 0,
            'eternal_approved': 0,
        },
        'findings': list()
    }

    # Get valid findings for the group
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group_name)
    are_findings_valid = await collect(
        findings_domain.validate_finding(str(finding['finding_id']))
        for finding in findings
    )
    valid_findings = [
        finding
        for finding, is_finding_valid in zip(findings, are_findings_valid)
        if is_finding_valid
    ]

    # Get stats
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    mail_context['findings'] = await get_oldest_open_findings(
        context, valid_findings, 3)
    treatments = await findings_domain.get_total_treatment_date(
        context, valid_findings, last_day)
    mail_context['treatments']['temporary_applied'] = treatments.get(
        'accepted', 0)
    mail_context['treatments']['eternal_requested'] = treatments.get(
        'accepted_undefined_submitted', 0)
    mail_context['treatments']['eternal_approved'] = treatments.get(
        'accepted_undefined_approved', 0)
    reattacks = await findings_domain.get_total_reattacks_stats(
        context, valid_findings, last_day)
    mail_context['reattacks']['reattacks_requested'] = reattacks.get(
        'reattacks_requested', 0)
    mail_context['reattacks']['reattacks_executed'] = reattacks.get(
        'reattacks_executed', 0)
    mail_context['reattacks']['pending_attacks'] = reattacks.get(
        'pending_attacks', 0)
    mail_context['reattack_effectiveness'] = reattacks.get(
        'reattack_effectiveness', 0)
    mail_context['queries'] = await get_total_comments_date(
        valid_findings, group_name, last_day)
    mail_context['remediation_time'] = int(
        await get_mean_remediate(context, group_name))
    mail_context['remediation_rate'] = await get_remediation_rate(
        context, group_name)

    return mail_context


async def sent_daily_digest(
    context: Any,
    group_name: str,
    mail_to: List[str],
) -> None:
    mail_context = await get_group_digest_stats(context, group_name)
    await schedule(groups_mail.send_mail_daily_digest(mail_to, mail_context))


async def main() -> None:
    """Daily Digest mail send to each analyst at the end of the day"""
    context = get_new_context()
    groups = FI_TEST_PROJECTS_DIGEST.split(',')
    mail_to = FI_MAIL_DIGEST.split(',')
    await collect([
        sent_daily_digest(context, group, mail_to)
        for group in groups
    ])
