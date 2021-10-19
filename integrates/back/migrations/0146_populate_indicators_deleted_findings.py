# pylint: disable=invalid-name
"""
Unreliable indicators were left out in the previous findings migration.
We need to populate them now for consistency and avoiding a StopIteration
with the group_removed_findings Dataloader.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    DynamoQuery as DynamoQueryType,
    Finding as FindingType,
    Historic as HistoricType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
)
from db_model.findings.utils import (
    format_treatment_summary_item,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy as dynamodb_ops,
)
from enum import (
    Enum,
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
import time
from typing import (
    cast,
    Dict,
    List,
)
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    _format_unreliable_status,
    _format_unreliable_treatment_summary,
)

FINDING_TABLE: str = "FI_findings"
PROD: bool = False


async def _update_unreliable_indicators(
    *,
    group_name: str,
    finding_id: str,
    indicators: FindingUnreliableIndicators,
) -> None:
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["finding_unreliable_indicators"],
        values={"group_name": group_name, "id": finding_id},
        is_removed=True,
    )
    unreliable_indicators = {
        key: value.value
        if isinstance(value, Enum)
        else format_treatment_summary_item(value)
        if isinstance(value, FindingTreatmentSummary)
        else value
        for key, value in indicators._asdict().items()
        if value is not None
    }
    await operations.update_item(
        item=unreliable_indicators,
        key=unreliable_indicators_key,
        table=TABLE,
    )


async def _calculate_unreliable_indicators(
    loaders: Dataloaders,
    finding_id: str,
) -> FindingUnreliableIndicators:
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

    return FindingUnreliableIndicators(
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


async def _proccess_finding(
    loaders: Dataloaders,
    old_finding: FindingType,
    progress: float,
) -> bool:
    finding_id: str = old_finding["finding_id"]
    group_name: str = old_finding["project_name"]

    indicators: FindingUnreliableIndicators = (
        await _calculate_unreliable_indicators(
            loaders=loaders,
            finding_id=finding_id,
        )
    )

    await _update_unreliable_indicators(
        group_name=group_name,
        finding_id=finding_id,
        indicators=indicators,
    )

    print(f'Progress: {round(progress, 4)} - "{group_name}" - "{finding_id}"')
    return True


def _filter_deleted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    return [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        == "DELETED"
    ]


async def main() -> None:
    success = False
    loaders: Dataloaders = get_new_context()

    # Scan old findings table
    start_time = datetime.now()
    scan_attrs: DynamoQueryType = {}
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)
    print(f"--- scan in {datetime.now() - start_time} ---")
    print(f"Scan findings: {len(findings)}")

    excluded_groups = ["worcester"]
    deleted_findings = [
        finding
        for finding in _filter_deleted_findings(findings)
        if finding.get("project_name", "") not in excluded_groups
    ]
    print(f"Deleted findings: {len(deleted_findings)}")

    if PROD:
        start_time = datetime.now()
        success = all(
            await collect(
                _proccess_finding(
                    loaders=loaders,
                    old_finding=old_finding,
                    progress=count / len(deleted_findings),
                )
                for count, old_finding in enumerate(deleted_findings)
            )
        )
        print(f"--- processing in {datetime.now() - start_time} ---")

    print(f"Success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
