# pylint: disable=invalid-name
"""
This migration aims to update the unreliable indicators facet for all
findings in alive groups in the single table vms

Related MR:
https://gitlab.com/fluidattacks/product/-/merge_requests/14700

Execution Time:    2021-10-06 at 18:48:38 UTCUTC
Finalization Time: 2021-10-06 at 19:01:42 UTCUTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicatorsToUpdate,
)
from findings.domain import (
    get_closed_vulnerabilities,
    get_is_verified,
    get_newest_vulnerability_report_date,
    get_oldest_open_vulnerability_report_date,
    get_oldest_vulnerability_report_date,
    get_open_vulnerabilities,
    get_status,
    get_treatment_summary,
    get_where,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
import time
from typing import (
    Tuple,
)
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    _format_unreliable_status,
    _format_unreliable_treatment_summary,
)

PROD: bool = True


async def _populate_finding_unreliable_indicator(
    loaders: Dataloaders,
    group_name: str,
    finding_id: str,
) -> None:
    indicators = {
        EntityAttr.closed_vulnerabilities: get_closed_vulnerabilities(
            loaders, finding_id
        )
    }
    indicators[EntityAttr.is_verified] = get_is_verified(loaders, finding_id)
    indicators[
        EntityAttr.newest_vulnerability_report_date
    ] = get_newest_vulnerability_report_date(loaders, finding_id)
    indicators[
        EntityAttr.oldest_open_vulnerability_report_date
    ] = get_oldest_open_vulnerability_report_date(loaders, finding_id)
    indicators[
        EntityAttr.oldest_vulnerability_report_date
    ] = get_oldest_vulnerability_report_date(loaders, finding_id)
    indicators[EntityAttr.open_vulnerabilities] = get_open_vulnerabilities(
        loaders, finding_id
    )
    indicators[EntityAttr.status] = get_status(loaders, finding_id)
    indicators[EntityAttr.where] = get_where(loaders, finding_id)
    indicators[EntityAttr.treatment_summary] = get_treatment_summary(
        loaders, finding_id
    )

    result = dict(zip(indicators.keys(), await collect(indicators.values())))

    indicators = FindingUnreliableIndicatorsToUpdate(
        unreliable_closed_vulnerabilities=result.get(
            EntityAttr.closed_vulnerabilities
        ),
        unreliable_is_verified=result.get(EntityAttr.is_verified),
        unreliable_newest_vulnerability_report_date=result.get(
            EntityAttr.newest_vulnerability_report_date
        ),
        unreliable_oldest_open_vulnerability_report_date=result.get(
            EntityAttr.oldest_open_vulnerability_report_date
        ),
        unreliable_oldest_vulnerability_report_date=result.get(
            EntityAttr.oldest_vulnerability_report_date
        ),
        unreliable_open_vulnerabilities=result.get(
            EntityAttr.open_vulnerabilities
        ),
        unreliable_status=_format_unreliable_status(
            result.get(EntityAttr.status)
        ),
        unreliable_where=result.get(EntityAttr.where),
        unreliable_treatment_summary=_format_unreliable_treatment_summary(
            result.get(EntityAttr.treatment_summary)
        ),
    )
    await findings_model.update_unreliable_indicators(
        group_name=group_name,
        finding_id=finding_id,
        indicators=indicators,
    )
    print(f"Indicators updated for {group_name} : {finding_id}")


async def main() -> None:
    success = False
    loaders: Dataloaders = get_new_context()
    alive_groups = {
        group["project_name"] for group in await groups_dal.get_alive_groups()
    }
    print(f"Alive groups: {len(alive_groups)}")
    group_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(alive_groups)
    findings = tuple(chain.from_iterable(group_findings))
    print(f"Findings: {len(findings)}")

    if PROD:
        success = all(
            await collect(
                _populate_finding_unreliable_indicator(
                    loaders=loaders,
                    group_name=finding.group_name,
                    finding_id=finding.id,
                )
                for finding in findings
            )
        )

    print(f"Success: {success}")

    return


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
