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
    Historic as HistoricType,
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


def filter_historic_last_day(historic: HistoricType) -> HistoricType:
    """Filter historics from the last 24 hrs"""
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    filtered = [
        entry
        for entry in historic
        if datetime_utils.get_from_str(entry['date']) >= last_day
    ]
    return filtered


async def get_total_reattacks_stats(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total reattacks of all the vulns"""
    reattacks_requested: int = 0
    reattacks_executed: int = 0
    pending_attacks: int = 0
    effective_reattacks: int = 0
    reattack_effectiveness: int = 0
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    finding_vulns_loader = context.finding_vulns_nzr

    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in findings
    ])

    for vuln in vulns:
        if vuln.get('last_requested_reattack_date', ''):
            last_requested_reattack_date = datetime_utils.get_from_str(
                vuln.get('last_requested_reattack_date', ''))
            if last_requested_reattack_date >= last_day:
                reattacks_requested += 1
        if vuln.get('last_reattack_date', ''):
            last_reattack_date = datetime_utils.get_from_str(
                vuln.get('last_reattack_date', ''))
            if last_reattack_date >= last_day:
                reattacks_executed += 1
                if vuln.get('current_state', '') == 'closed':
                    effective_reattacks += 1
        if vuln.get('verification', '') == 'Requested':
            pending_attacks += 1

    if reattacks_executed:
        reattack_effectiveness = int(
            100 * effective_reattacks / reattacks_executed)

    return {
        'reattacks_requested': reattacks_requested,
        'reattacks_executed': reattacks_executed,
        'pending_attacks': pending_attacks,
        'reattack_effectiveness': reattack_effectiveness,
    }


async def get_total_treatment_stats(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total treatment of all the vulns"""
    accepted_vuln: int = 0
    accepted_undefined_submited_vuln: int = 0
    accepted_undefined_approved_vuln: int = 0
    finding_vulns_loader = context.finding_vulns_nzr

    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in findings
    ])

    for vuln in vulns:
        filtered_historic_as_str = str(filter_historic_last_day(
            vuln.get('historic_treatment', [{}])))
        # Check if any of these states occurred in the period
        if '\'ACCEPTED\'' in filtered_historic_as_str:
            accepted_vuln += 1
        if 'SUBMITTED' in filtered_historic_as_str:
            accepted_undefined_submited_vuln += 1
        if 'APPROVED' in filtered_historic_as_str:
            accepted_undefined_approved_vuln += 1
    return {
        'accepted': accepted_vuln,
        'accepted_undefined_submitted': accepted_undefined_submited_vuln,
        'accepted_undefined_approved': accepted_undefined_approved_vuln,
    }


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
    treatments = await get_total_treatment_stats(context, valid_findings)
    mail_context['treatments']['temporary_applied'] = treatments.get(
        'accepted', 0)
    mail_context['treatments']['eternal_requested'] = treatments.get(
        'accepted_undefined_submitted', 0)
    mail_context['treatments']['eternal_approved'] = treatments.get(
        'accepted_undefined_approved', 0)
    reattacks = await get_total_reattacks_stats(context, valid_findings)
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
