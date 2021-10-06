# pylint: disable=invalid-name
"""
This migration aims to merge duplicate findings generated during the
standarization titles migration (0102).

Vulns are copied to the oldest finding and the newer ones is deleted.

Duplicate vulns in the merged finding are also deleted.

Execution Time:    2021-07-30 at 18:03:54 UTC-05
Finalization Time: 2021-07-30 at 18:04:25 UTC-05

Execution Time:    2021-08-03 at 09:41:31 UTC-05
Finalization Time: 2021-08-03 at 09:56:04 UTC-05

Execution Time:    2021-08-03 at 14:46:19 UTC-05
Finalization Time: 2021-08-03 at 14:46:25 UTC-05

Execution Time:    2021-08-04 at 11:46:10 UTC-05
Finalization Time: 2021-08-04 at 11:46:32 UTC-05

Execution Time:    2021-08-04 at 18:22:33 UTC-05
Finalization Time: 2021-08-04 at 18:31:30 UTC-05

Execution Time:    2021-08-05 at 09:02:12 UTC-05
Finalization Time: 2021-08-05 at 09:35:52 UTC-05

Execution Time:    2021-08-05 at 16:19:04 UTC-05
Finalization Time: 2021-08-05 at 16:26:03 UTC-05

Execution Time:    2021-08-05 at 18:37:39 UTC-05
Finalization Time: 2021-08-05 at 18:37:45 UTC-05

Execution Time:    2021-08-06 at 09:01:37 UTC-05
Finalization Time: 2021-08-06 at 09:44:39 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import copy
import csv
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
    Vulnerability as VulnType,
)
from findings import (
    dal as findings_dal,
)
from newutils import (
    findings as findings_utils,
    vulnerabilities as vulns_utils,
)
from operator import (
    itemgetter,
)
import time
from typing import (
    cast,
    Dict,
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)
from vulnerabilities.domain.utils import (
    get_hash_from_dict,
)

PROD: bool = True


def _get_creation_date(vuln: Dict[str, VulnType]) -> str:
    historic_state = cast(HistoricType, vuln.get("historic_state", [{}]))
    return historic_state[0].get("date", "")


async def remove_duplicate_vulns(
    finding_id: str,
) -> bool:
    vulns = await vulns_dal.get_by_finding(finding_id)
    open_vulns = [
        vuln for vuln in vulns if vulns_utils.get_last_status(vuln) == "open"
    ]

    duplicates: List[Dict[str, FindingType]] = [
        next(
            iter(
                [
                    vuln
                    for vuln in open_vulns
                    if vuln["UUID"] != vuln_to_compare["UUID"]
                    and get_hash_from_dict(vuln)
                    == get_hash_from_dict(vuln_to_compare)
                    and vuln.get("repo_nickname", "no_repo1")
                    == vuln_to_compare.get("repo_nickname", "no_repo2")
                    and _get_creation_date(vuln)
                    >= _get_creation_date(vuln_to_compare)
                ]
            ),
            {},
        )
        for vuln_to_compare in open_vulns
    ]
    duplicates = [vuln for vuln in duplicates if vuln]
    duplicates = sorted(duplicates, key=itemgetter("where"), reverse=True)

    if not len(duplicates):  # noqa
        print(f"   === {finding_id}, NO duplicates found")
        return True

    print(f"   === {finding_id}, duplicates found ({len(duplicates)})")
    success = False
    if PROD:
        success = all(
            await collect(
                vulns_dal.delete(vuln["UUID"], finding_id)
                for vuln in duplicates
            )
        )
        print(f"   === {finding_id}, duplicates removed: {success}")

    return success


def _get_approval_date(finding: Dict[str, FindingType]) -> str:
    """Get approval date from the historic state"""
    approval_date = "ZZZ"
    approval_info = None
    historic_state = findings_utils.get_historic_state(finding)
    if historic_state:
        approval_info = list(
            filter(
                lambda state_info: state_info["state"] == "APPROVED",
                historic_state,
            )
        )
    if approval_info:
        approval_date = approval_info[-1]["date"]
    return approval_date


async def merge_findings(
    finding_id1: str,
    finding_id2: str,
) -> str:
    finding1 = await findings_dal.get_finding(finding_id1)
    finding2 = await findings_dal.get_finding(finding_id2)

    if not finding1:
        print(f"   ### ERROR finding1 NOT in db ({finding_id1})")
        return finding_id2
    if not finding2:
        print(f"   ### ERROR finding2 NOT in db ({finding_id2})")
        return finding_id1

    # Find oldest finding and call it "target"
    release_date1 = _get_approval_date(finding1)
    release_date2 = _get_approval_date(finding2)
    if release_date1 < release_date2:
        target_finding = finding_id1  # Older
        duplicate_finding = finding_id2  # Newer
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
        print(f"   --- {target_finding}, vulns created: {success}")
        # Delete old ones
        if success:
            success = all(
                await collect(
                    vulns_dal.delete(vuln["UUID"], vuln["finding_id"])
                    for vuln in vulns_to_move
                )
            )
            print(f"   --- {duplicate_finding}, vulns deleted: {success}")
            if success:
                vulns_left = await vulns_dal.get_by_finding(duplicate_finding)
                print(f"   === vulns_left: {len(vulns_left)}")
                if not vulns_left:
                    # Remove duplicate finding once it's empty
                    success = await findings_dal.delete(duplicate_finding)
                    print(
                        f"   --- {duplicate_finding}, finding deleted: "
                        f"{str(success)}"
                    )

    return target_finding


async def process_row(row: List[str]) -> bool:
    merged_finding_id = await merge_findings(row[0], row[1])

    if len(row) > 2 and row[2]:
        print(f"   === finding3 ({row[2]}) present")
        merged_finding_id = await merge_findings(merged_finding_id, row[2])

    if merged_finding_id:
        return await remove_duplicate_vulns(merged_finding_id)
    return False


async def main() -> None:
    success = False

    # Read findings info
    with open("0114.csv", mode="r", encoding="utf8") as infile:
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
