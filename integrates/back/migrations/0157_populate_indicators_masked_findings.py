# pylint: disable=invalid-name
"""
This migration aims to populate the unreliable indicators for findings
in "removed" groups.
These indicators were left out in the previous findings migration.
We need to populate them now for consistency and avoiding a StopIteration
when masked findings are needed to be read.

Execution Time:     2021-11-03 at 03:00:26 UTC
Finalization Time:  2021-11-03 at 03:22:55 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
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
from groups import (
    dal as groups_dal,
)
import time
from typing import (
    Set,
)
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    _format_unreliable_status,
    _format_unreliable_treatment_summary,
)

PROD: bool = True


# Get both drafts and findings
async def _get_finding_ids_by_group(
    group_name: str,
) -> Set[str]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_metadata"],),
        index=index,
        table=TABLE,
    )
    return {
        str(item[key_structure.sort_key]).split("#")[1] for item in results
    }


async def _update_unreliable_indicators(
    *,
    group_name: str,
    finding_id: str,
    indicators: FindingUnreliableIndicators,
) -> None:
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["finding_unreliable_indicators"],
        values={"group_name": group_name, "id": finding_id},
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
    finding_id: str,
    group_name: str,
    loaders: Dataloaders,
) -> None:
    indicators: FindingUnreliableIndicators = (
        await _calculate_unreliable_indicators(
            loaders=loaders,
            finding_id=finding_id,
        )
    )
    if PROD:
        await _update_unreliable_indicators(
            group_name=group_name,
            finding_id=finding_id,
            indicators=indicators,
        )
    print(f'Indicators OK - "{group_name}" - "{finding_id}"')


async def _process_group(
    group_name: str,
    loaders: Dataloaders,
) -> None:
    finding_ids = await _get_finding_ids_by_group(group_name)
    print(f"{str(group_name)} : {len(finding_ids)} findings")
    await collect(
        _proccess_finding(
            finding_id=finding_id,
            group_name=group_name,
            loaders=loaders,
        )
        for finding_id in finding_ids
    )


async def main() -> None:
    filtering_exp = (
        Attr("project_status").eq("DELETED")
        | Attr("project_status").eq("FINISHED")
        | Attr("project_status").eq("PENDING_DELETION")
    )
    masked_groups = sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )
    print(f"Masked groups: {len(masked_groups)}")

    start_time = datetime.now()
    loaders: Dataloaders = get_new_context()
    await collect(
        _process_group(
            group_name=group_name,
            loaders=loaders,
        )
        for group_name in masked_groups
    )
    print(f"--- processing in {datetime.now() - start_time} ---")
    print("Done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
