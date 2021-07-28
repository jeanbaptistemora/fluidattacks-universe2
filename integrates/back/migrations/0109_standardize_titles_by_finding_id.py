# pylint: disable=invalid-name
"""
This migration aims to standardize all findings titles, found in:
https://gitlab.com/fluidattacks/product/-/blob/master/makes/makes/criteria/src/vulnerabilities/data.yaml

In this case, we take a finding_id and update its title directly from the csv

Execution Time:    2021-07-28 at 15:26:37 UTC-05
Finalization Time: 2021-07-28 at 15:26:39 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from findings import (
    dal as findings_dal,
)
import time

PROD: bool = True
TABLE_NAME: str = "FI_findings"


async def main() -> None:
    # Read migration matchs
    with open("0109_findings_info.csv", mode="r") as infile:
        reader = csv.reader(infile)
        findings = [
            {
                "finding_id": rows[1],
                "title": rows[4],
            }
            for rows in reader
            if rows[1] != "finding_id"
        ]

    print(f"    === findings to update: {len(findings)}")
    print(f"    === sample: {findings[:3]}")

    success = False
    if PROD:
        success = all(
            await collect(
                findings_dal.update(
                    finding["finding_id"],
                    {
                        "finding": finding["title"],
                    },
                )
                for finding in findings
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
