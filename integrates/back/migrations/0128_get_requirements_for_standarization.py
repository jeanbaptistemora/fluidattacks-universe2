# pylint: disable=invalid-name
"""
This migration aims to get info about the current data in the requirements
field, for all the findings in db.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/5229

Execution Time:    2021-08-26 at 10:10:31 UTC-05
Finalization Time: 2021-08-26 at 10:13:07 UTC-05
"""

from aioextensions import (
    run,
)
import csv
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from groups.dal import (
    get_active_groups,
)
from newutils.findings import (
    filter_non_deleted_findings,
)
import time
from typing import (
    cast,
    List,
)

TABLE_NAME: str = "FI_findings"


async def _get_all_findings(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[FindingType]:
    """Get all findings in DB"""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return cast(List[FindingType], items)


def _get_source(
    finding: FindingType,
) -> str:
    source = ""
    historic_state: HistoricType = finding["historic_state"]
    if historic_state:
        source = historic_state[0].get("source", "")
    return source


async def main() -> None:
    active_groups = sorted(await get_active_groups())
    print(f"    === active groups ({len(active_groups)})")
    findings = await _get_all_findings()
    print(f"    === findings (all) in db: {len(findings)}")
    findings_non_deleted = [
        {
            "group": finding["project_name"],
            "finding_id": finding["finding_id"],
            "title": finding["finding"],
            "requirements": str(finding.get("requirements", "")).strip(),
            "description": finding.get("vulnerability", ""),
            "impacts": finding.get("attack_vector_desc", ""),
            "recommendation": finding.get("effect_solution", ""),
            "threat": finding.get("threat", ""),
            "source": _get_source(finding),
        }
        for finding in filter_non_deleted_findings(findings)
        if str(finding.get("project_name", "")).strip()
        and finding["project_name"] in active_groups
    ]
    print(f"    === findings (non deleted) in db: {len(findings_non_deleted)}")
    print(f"    === sample: {findings_non_deleted[0:3]}")

    csv_columns = [
        "group",
        "finding_id",
        "title",
        "requirements",
        "description",
        "impacts",
        "recommendation",
        "threat",
        "source",
    ]
    csv_file = "0128_2021_aug_26.csv"
    success = False
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in findings_non_deleted:
                writer.writerow(data)
        success = True
    except IOError:
        print("     === I/O error")

    print(f"    === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
