from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def send_group_treatment_change(
    context: Dataloaders, group_name: str, min_date: datetime
) -> None:
    group_findings_loader = context.group_findings
    group_findings = await group_findings_loader.load(group_name)
    findings = [
        {
            "finding_id": finding["finding_id"],
            "title": finding["title"],
        }
        for finding in group_findings
    ]
    await collect(
        vulns_domain.send_treatment_change_mail(
            context,
            finding["finding_id"],
            finding["title"],
            group_name,
            min_date,
        )
        for finding in findings
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
