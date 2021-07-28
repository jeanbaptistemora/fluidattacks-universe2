# pylint: disable=invalid-name
"""
This migration aims only to get finding's titles before migration
"0102_standardize_findings_titles".

A backup has been restored for table "FI_findings", time Jul 22 2021

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:
Finalization Time:
"""

from aioextensions import (
    run,
)
import csv
from custom_types import (
    Finding,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from newutils.findings import (
    filter_non_deleted_findings,
)
import time
from typing import (
    cast,
    List,
)

TABLE_NAME: str = "Backup_findings_22Jul"


async def get_all_findings(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[Finding]:
    """Get all findings in DB"""
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(TABLE_NAME, scan_attrs)
    return cast(List[Finding], items)


async def main() -> None:
    findings = await get_all_findings()
    print(f"    === findings (all) in db: {len(findings)}")
    findings_non_deleted = [
        {
            "group": finding["project_name"],
            "finding_id": finding["finding_id"],
            "finding_name": finding["finding"],
        }
        for finding in filter_non_deleted_findings(findings)
        if str(finding.get("project_name", "")).strip()
        and str(finding.get("finding", "")).strip()
    ]
    print(f"    === findings (non deleted) in db: {len(findings_non_deleted)}")
    print(f"    === sample: {findings_non_deleted[0:3]}")

    csv_columns = ["group", "finding_id", "finding_name"]
    csv_file = "0108_findings_names_jul_22_2021.csv"
    success = False
    try:
        with open(csv_file, "w") as f:
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
