# pylint: disable=invalid-name
"""
This migration aims to merge duplicated findings generated during the
standarization titles migration (0102).

Vulns are copied to the oldest finding and the newer ones is deleted.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
import copy
import csv
from findings import (
    dal as findings_dal,
    domain as findings_domain,
)
from newutils import (
    findings as findings_utils,
)
import time
from typing import (
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = True


async def merge_findings(
    finding_id1: str,
    finding_id2: str,
) -> str:
    findings = await findings_domain.get_findings_async(
        [finding_id1, finding_id2]
    )
    # Find oldest finding and call it "target"
    release_date1 = findings_utils.get_approval_date(findings[0])
    release_date2 = findings_utils.get_approval_date(findings[1])
    if release_date1 < release_date2:
        target_finding = finding_id1
        duplicate_finding = finding_id2
        release_date = release_date1
    else:
        target_finding = finding_id2
        duplicate_finding = finding_id1
        release_date = release_date2

    print(
        f"target ({release_date}): {target_finding}, "
        f"duplicate: {duplicate_finding}"
    )

    vulns_to_move = await vulns_dal.get_by_finding(duplicate_finding)

    new_vulns = copy.deepcopy(vulns_to_move)
    for vuln in new_vulns:
        vuln["finding_id"] = target_finding

    uuids = [vuln["UUID"] for vuln in vulns_to_move]
    print(f"   === vulns_to_move ({len(uuids)}): {uuids}")
    print(f"   === new_vulns sample: {new_vulns[:1]}")

    if PROD:
        # Create new ones
        success = all(
            await collect(vulns_dal.create(vuln) for vuln in new_vulns)
        )
        print(f"   --- created: {success}")
        # Delete old ones
        if success:
            success = all(
                await collect(
                    vulns_dal.delete(vuln["UUID"], vuln["finding_id"])
                    for vuln in vulns_to_move
                )
            )
            print(f"   --- deleted: {success}")
            if success:
                vulns_left = await vulns_dal.get_by_finding(duplicate_finding)
                print(f"   === vulns_left: {len(vulns_left)}")
                if not vulns_left:
                    # Remove duplicate finding once it's empty
                    success = await findings_dal.delete(duplicate_finding)
                    print(
                        f"   >>> finding {duplicate_finding} deleted: "
                        f"{str(success)}"
                    )

    return target_finding


async def process_row(row: List[str]) -> bool:
    merged_finding_id = await merge_findings(row[0], row[1])

    if len(row) > 2 and row[2]:
        print(row[2] + " present!!!")
        await merge_findings(merged_finding_id, row[2])

    return True


async def main() -> None:
    success = False

    # Read findings info
    with open("0114.csv", mode="r") as infile:
        reader = csv.reader(infile)
        to_merge = [[rows[0], rows[1], rows[2]] for rows in reader]

    print(f"   === to_merge: {len(to_merge)}:\n{to_merge}")

    success = all(await collect(process_row(row) for row in to_merge))

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
