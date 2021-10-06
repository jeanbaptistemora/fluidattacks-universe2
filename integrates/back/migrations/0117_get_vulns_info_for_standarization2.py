# pylint: disable=invalid-name
"""
Extract info related to vulns from a csv list for finding
standarization purposes

Execution Time:    2021-08-10 at 10:03:07 UTC-05
Finalization Time: 2021-08-10 at 10:03:53 UTC-05

Execution Time:    2021-08-18 at 17:05:21 UTC-05
Finalization Time: 2021-08-18 at 17:06:47 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from newutils.vulnerabilities import (
    get_last_status,
)
import time
from typing import (
    Dict,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = False


async def get_vuln_status(vuln_uuid: str) -> Dict[str, str]:
    vuln = await vulns_dal.get(vuln_uuid)
    last_status = get_last_status(vuln[0])
    if not last_status:
        last_status = "NOT_FOUND"
    return {
        "vuln_uuid": vuln_uuid,
        "vuln_status": last_status,
    }


async def main() -> None:
    # Read file with uuids
    with open("0117.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        vulns_uuids = [row[0] for row in reader]
    print(f"    === vulns uuids: {len(vulns_uuids)}")
    print(f"    === sample: {vulns_uuids[:3]}")

    info = await collect(
        [get_vuln_status(vuln_uuid) for vuln_uuid in vulns_uuids]
    )

    csv_columns = [
        "vuln_uuid",
        "vuln_status",
    ]
    csv_file = "0117_results.csv"
    success = False
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in info:
                writer.writerow(data)
        success = True
    except IOError:
        print("   === I/O error")

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z",
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z",
    )
    print(f"{execution_time}\n{finalization_time}")
