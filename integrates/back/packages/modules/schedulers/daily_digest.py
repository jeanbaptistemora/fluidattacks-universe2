# Standard libraries
import logging
import logging.config
from typing import (
    Any,
    cast,
    Counter,
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
from mailer import groups as groups_mail
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    vulnerabilities as vulns_utils,
)
from newutils.findings import (
    get_state_actions,
)
from __init__ import (
    FI_MAIL_DIGEST,
    FI_TEST_PROJECTS_DIGEST,
)


bugsnag_utils.start_scheduler_session()

LOGGER = logging.getLogger(__name__)


async def get_total_treatment_stats(  # pylint: disable=too-many-locals
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total treatment of all the vulns"""
    accepted_vuln: int = 0
    accepted_undefined_vuln: int = 0
    accepted_undefined_submited_vuln: int = 0
    accepted_undefined_approved_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    finding_vulns_loader = context.finding_vulns_nzr

    vulns = await finding_vulns_loader.load_many_chained([
        str(finding['finding_id'])
        for finding in findings
    ])

    for vuln in vulns:
        vuln_treatment = cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )[-1].get('treatment')
        vuln_acceptance_status = cast(
            List[Dict[str, str]],
            vuln.get('historic_treatment', [{}])
        )[-1].get('acceptance_status')
        current_state = vulns_utils.get_last_status(vuln)
        open_vuln: int = 1 if current_state == 'open' else 0
        if vuln_treatment == 'ACCEPTED':
            accepted_vuln += open_vuln
        elif vuln_treatment == 'ACCEPTED_UNDEFINED':
            accepted_undefined_vuln += open_vuln
            if vuln_acceptance_status == 'SUBMITTED':
                accepted_undefined_submited_vuln += open_vuln
            elif vuln_acceptance_status == 'APPROVED':
                accepted_undefined_approved_vuln += open_vuln
        elif vuln_treatment == 'IN PROGRESS':
            in_progress_vuln += open_vuln
        else:
            undefined_treatment += open_vuln
    return {
        'accepted': accepted_vuln,
        'accepted_undefined': accepted_undefined_vuln,
        'accepted_undefined_submitted': accepted_undefined_submited_vuln,
        'accepted_undefined_approved': accepted_undefined_approved_vuln,
        'in_progress': in_progress_vuln,
        'undefined': undefined_treatment,
    }


async def get_findings_new_vulns(
    context: Any,
    findings: List[Dict[str, FindingType]]
) -> list:
    """Get the findings with open vulns"""
    try:
        new_vulns: List[Dict[str, str]] = list()
        last_day = datetime_utils.get_now_minus_delta(hours=24)
        finding_vulns_loader = context.finding_vulns_nzr
        for finding in findings:
            vulns = await finding_vulns_loader.load(str(finding['finding_id']))
            states_actions = get_state_actions(vulns)
            actions = list(filter(
                lambda action: (
                    datetime_utils.get_from_str(
                        action.date, '%Y-%m-%d') >= last_day
                ),
                states_actions
            ))
            state_counter: Counter[str] = sum(
                [Counter({action.action: action.times}) for action in actions],
                Counter()
            )
            if state_counter['open']:
                new_vulns.append({
                    'finding_name': finding['finding'],
                    'finding_number': str(state_counter['open']),
                })
        return new_vulns
    except (TypeError, KeyError) as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise


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
    mail_context['treatments']['pending_attacks'] = treatments.get(
        'accepted_undefined_approved', 0)
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
