# pylint: disable=invalid-name
"""
Extract info related to vulns from a csv list for finding
standarization purposes

Execution Time:    2021-08-10 at 10:03:07 UTC-05
Finalization Time: 2021-08-10 at 10:03:53 UTC-05
"""

from aioextensions import (
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from newutils.vulnerabilities import (
    get_last_status,
)
import time

PROD: bool = False


async def main() -> None:
    # Read file with uuids
    with open("0117.csv", mode="r") as f:
        reader = csv.reader(f)
        vulns_uuids = [row[0] for row in reader]
    print(f"    === vulns uuids: {len(vulns_uuids)}")
    print(f"    === sample: {vulns_uuids[:3]}")

    context: Dataloaders = get_new_context()
    vuln_loader = context.vulnerability
    vulns = await vuln_loader.load_many(vulns_uuids)

    info = [
        {
            "vuln_uuid": vuln["id"],
            "vuln_status": get_last_status(vuln),
        }
        for vuln in vulns
    ]

    csv_columns = [
        "vuln_uuid",
        "vuln_status",
    ]
    csv_file = "0117_vuln_info_aug_10.csv"
    success = False
    try:
        with open(csv_file, "w") as f:
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
