# pylint: disable=invalid-name
"""
This migration removes findings with no vulns after
migration "0105_delete_duplicated_vulns"
https://gitlab.com/fluidattacks/product/-/issues/5068

Execution Time:    2021-07-26 at 19:43:02 UTC-05
Finalization Time: 2021-07-26 at 19:47:13 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    get_new_context,
)
from findings import (
    dal as findings_dal,
)
import time

PROD: bool = True


async def main() -> None:
    # Read file with deletion info
    with open("0106_findings_to_delete.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        findings_to_check = [row[0] for row in reader]
    print(f"    === findings to check: {len(findings_to_check)}")

    # Filter findings with no vulns in db
    context = get_new_context()
    finding_vulns_all_loader = context.finding_vulns_all
    findings_to_delete = [
        finding
        for finding in findings_to_check
        if len(await finding_vulns_all_loader.load(finding)) == 0
    ]
    print(f"    === findings to delete: {len(findings_to_delete)}")

    success = False
    if PROD:
        success = all(
            await collect(
                findings_dal.delete(finding) for finding in findings_to_delete
            )
        )

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
