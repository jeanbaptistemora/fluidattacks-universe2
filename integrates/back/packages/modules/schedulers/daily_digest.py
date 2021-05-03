# Standard libraries
import logging
import logging.config
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
from mailer import groups as groups_mail
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
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
        if datetime_utils.get_from_str(entry.get('date')) >= last_day
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
    last_day = datetime_utils.get_now_minus_delta(hours=24)
    finding_vulns_loader = context.finding_vulns_nzr

    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in findings
    ])

    for vuln in vulns:
        if vuln.get('last_requested_reattack_date'):
            last_requested_reattack_date = datetime_utils.get_from_str(
                vuln.get('last_requested_reattack_date'))
            if last_requested_reattack_date >= last_day:
                reattacks_requested += 1
        if vuln.get('last_reattack_date'):
            last_reattack_date = datetime_utils.get_from_str(
                vuln.get('last_reattack_date'))
            if last_reattack_date >= last_day:
                reattacks_executed += 1
        if vuln.get('verification', '') == 'Requested':
            pending_attacks += 1
    return {
        'reattacks_requested': reattacks_requested,
        'reattacks_executed': reattacks_executed,
        'pending_attacks': pending_attacks,
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


async def get_findings_new_vulns(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> list:
    """Get the findings with open vulns in last 24 hrs"""
    finding_vulns_loader = context.finding_vulns_nzr
    new_vulns: List[Dict[str, str]] = list()

    for finding in findings:
        vulns = await finding_vulns_loader.load(str(finding['finding_id']))
        vulns_counter: int = 0
        for vuln in vulns:
            filtered_state = filter_historic_last_day(
                vuln.get('historic_state', [{}]))
            if 'open' in str(filtered_state):
                vulns_counter += 1
        if vulns_counter:
            new_vulns.append({
                'finding_name': finding['finding'],
                'finding_number': str(vulns_counter),
            })
    return new_vulns


async def get_group_statistics(context: Any, group_name: str) -> None:
    # Most of the following statistics are yet to be calculated, however, the
    # fields in mail_context are needed for rendering the initial mail
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
    mail_context['findings'] = await get_findings_new_vulns(
        context, valid_findings)
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
    mail_to = FI_MAIL_DIGEST.split(',')

    await schedule(groups_mail.send_mail_daily_digest(mail_to, mail_context))


async def main() -> None:
    """Daily Digest mail send to each analyst at the end of the day"""
    context = get_new_context()
    groups = FI_TEST_PROJECTS_DIGEST.split(',')
    await collect([
        get_group_statistics(context, group)
        for group in groups
    ])
