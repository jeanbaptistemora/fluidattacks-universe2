# pylint: disable=invalid-name
"""
This migration aims to standardize all findings titles, found in:
https://gitlab.com/fluidattacks/product/-/blob/master/makes/makes/criteria/src/vulnerabilities/data.yaml

Currently all in english

Execution Time:     2021-07-22 at 17:42:27 UTC-05
Finalization Time:  2021-07-22 at 18:32:18 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_types import (
    Finding,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from findings import (
    dal as findings_dal,
)
import time
from typing import (
    cast,
    List,
)

PROD: bool = True
TABLE_NAME: str = "FI_findings"


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
    # Read new titles alone
    with open("0102_new_titles_only.txt", encoding="utf8") as f:
        new_titles = f.read().splitlines()

    # Read migration matchs
    with open("0102_findings_titles.csv", mode="r", encoding="utf8") as infile:
        reader = csv.reader(infile)
        typologies_migration = {rows[0]: rows[1] for rows in reader}

    print(f"    === titles to match: {len(typologies_migration)}")

    # Get findings to update and
    # Print findings whose title does not match
    findings = await get_all_findings()
    print(f"    === findings in db: {len(findings)}")
    findings_to_update = []
    for finding in findings:
        title = str(finding.get("finding", "")).strip()
        if title in new_titles:
            # Ignored, already migrated
            continue
        if (
            not title
            or title == "WIPED"
            or title.startswith("SKIMS")
            or "please" in title
        ):
            # Ignored
            continue
        if title not in typologies_migration:
            print(f'ERROR: {finding["finding_id"]}, {title}')
            # Ignored, title does not match
            continue
        findings_to_update.append(finding)

    print(f"    === findings to update: {len(findings_to_update)}")

    success = False
    if PROD:
        success = all(
            await collect(
                findings_dal.update(
                    finding["finding_id"],
                    {
                        "finding": typologies_migration[
                            str(finding["finding"]).strip()
                        ]
                    },
                )
                for finding in findings_to_update
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
