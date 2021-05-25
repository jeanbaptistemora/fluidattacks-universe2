from datetime import datetime
from typing import Any

from aioextensions import collect

from dataloaders import get_new_context
from findings import domain as findings_domain
from groups import domain as groups_domain
from newutils import datetime as datetime_utils
from vulnerabilities import domain as vulns_domain


async def send_group_treatment_change(
    context: Any, group_name: str, min_date: datetime
) -> None:
    findings = await findings_domain.list_findings(context, [group_name])
    await collect(
        vulns_domain.send_treatment_change_mail(context, finding_id, min_date)
        for finding_id in findings[0]
    )


async def send_treatment_change() -> None:
    context = get_new_context()
    groups = await groups_domain.get_active_groups()
    min_date = datetime_utils.get_now_minus_delta(days=1)
    await collect(
        [
            send_group_treatment_change(context, group_name, min_date)
            for group_name in groups
        ],
        workers=20,
    )


async def main() -> None:
    await send_treatment_change()
