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
from db_model.findings.types import (
    Finding,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Tuple,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def send_group_treatment_change(
    loaders: Dataloaders, group_name: str, min_date: datetime
) -> None:
    group_findings_loader = loaders.group_findings_new
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    await collect(
        vulns_domain.send_treatment_change_mail(
            loaders,
            finding.id,
            finding.title,
            group_name,
            min_date,
        )
        for finding in group_findings
    )


async def send_treatment_change() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await groups_domain.get_active_groups()
    min_date = datetime_utils.get_now_minus_delta(days=1)
    await collect(
        [
            send_group_treatment_change(loaders, group_name, min_date)
            for group_name in groups
        ],
        workers=20,
    )


async def main() -> None:
    await send_treatment_change()
