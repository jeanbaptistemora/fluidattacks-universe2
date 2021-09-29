# pylint: disable=invalid-name
"""
This migration aims to standardize all findings titles, found in:
https://gitlab.com/fluidattacks/product/-/blob/master/makes/makes/criteria/src/vulnerabilities/data.yaml

In this case, we take a finding_id and update its title directly from the csv

Execution Time:    2021-07-28 at 15:26:37 UTC-05
Finalization Time: 2021-07-28 at 15:26:39 UTC-05

Execution Time:    2021-07-29 at 18:24:08 UTC-05
Finalization Time: 2021-07-29 at 18:30:17 UTC-05

Execution Time:    2021-08-03 at 10:08:59 UTC-05
Finalization Time: 2021-08-03 at 10:09:00 UTC-05

Execution Time:    2021-08-03 at 14:41:00 UTC-05
Finalization Time: 2021-08-03 at 14:41:01 UTC-05

Execution Time:    2021-08-04 at 11:20:03 UTC-05
Finalization Time: 2021-08-04 at 11:20:04 UTC-05

Execution Time:    2021-08-04 at 18:06:11 UTC-05
Finalization Time: 2021-08-04 at 18:06:20 UTC-05

Execution Time:    2021-08-05 at 09:38:21 UTC-05
Finalization Time: 2021-08-05 at 09:38:22 UTC-05

Execution Time:    2021-08-05 at 14:30:30 UTC-05
Finalization Time: 2021-08-05 at 14:30:31 UTC-05

Execution Time:    2021-08-05 at 16:35:22 UTC-05
Finalization Time: 2021-08-05 at 16:37:16 UTC-05

Execution Time:    2021-08-05 at 18:39:54 UTC-05
Finalization Time: 2021-08-05 at 18:39:55 UTC-05

Execution Time:    2021-08-06 at 08:54:02 UTC-05
Finalization Time: 2021-08-06 at 08:57:04 UTC-05

Execution Time:    2021-08-06 at 11:38:02 UTC-05
Finalization Time: 2021-08-06 at 11:38:20 UTC-05

Execution Time:    2021-09-29 at 16:34:59 UTCUTC
Finalization Time: 2021-09-29 at 16:35:53 UTCUTC
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
    with open("0109.csv", mode="r") as infile:
        reader = csv.reader(infile)
        findings = [
            {
                "finding_id": rows[0],
                "title": rows[1],
            }
            for rows in reader
            if rows[0] != "finding_id"
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
