# Standard libraries
import logging
import logging.config
from typing import (
    Any,
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
from backend import mailer
from backend.api import get_new_context
from backend.typing import (
    MailContent as MailContentType,
)
from groups import domain as groups_domain
from group_access import domain as group_access_domain
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
)
from newutils.findings import (
    get_state_actions,
)


bugsnag_utils.start_scheduler_session()

LOGGER = logging.getLogger(__name__)


async def get_findings_new_vulns(context: Any, group_name: str) -> list:
    group_findings_loader = context.group_findings
    try:
        new_vulns: List[Dict[str, str]] = list()
        findings = await group_findings_loader.load(group_name)
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
        LOGGER.exception(ex, extra={'extra': {'group_name': group_name}})
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
    mail_context['findings'] = await get_findings_new_vulns(
        context, group_name)
    mail_to = await group_access_domain.get_users_to_notify(group_name)
    schedule(
        mailer.send_mail_daily_digest(mail_to, mail_context)
    )


async def main() -> None:
    """Daily Digest mail send to each analyst at the end of the day"""
    context = get_new_context()
    groups = await groups_domain.get_active_groups()
    await collect([
        get_group_statistics(context, group)
        for group in groups
    ])
