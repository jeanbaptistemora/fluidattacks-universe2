# pylint: disable=invalid-name
"""
This migration will move vulns to a designated finding for
standarization purposes. The vulns info is loaded from a csv file.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-12 at 13:47:57 UTC-05
Finalization Time: 2021-08-12 at 13:57:28 UTC-05

Execution Time:    2021-08-19 at 11:26:04 UTC-05
Finalization Time: 2021-08-19 at 11:26:11 UTC-05

Execution Time:    2021-08-20 at 21:22:35 UTC-05
Finalization Time: 2021-08-20 at 21:33:36 UTC-05

Execution Time:    2021-08-23 at 10:03:40 UTC-05
Finalization Time: 2021-08-23 at 11:55:16 UTC-05

Execution Time:    2021-08-23 at 14:28:26 UTC-05
Finalization Time: 2021-08-23 at 16:08:33 UTC-05

Execution Time:    2021-08-24 at 09:43:47 UTC-05
Finalization Time: 2021-08-24 at 11:21:55 UTC-05

Execution Time:    2021-08-24 at 12:18:52 UTC-05
Finalization Time: 2021-08-24 at 13:04:48 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import time
from typing import (
    Dict,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = True


async def process_vuln(
    context: Dataloaders,
    vuln_info: Dict[str, str],
) -> bool:
    group_name = vuln_info["group_name"]
    target_finding = {}

    group_findings_loader = context.group_findings
    group_findings = await group_findings_loader.load(group_name)
    group_findings_titles = [finding["title"] for finding in group_findings]
    if vuln_info["definitive_name"] in group_findings_titles:
        target_finding = next(
            finding
            for finding in group_findings
            if finding["title"] == vuln_info["definitive_name"]
        )
    else:
        group_drafts_loader = context.group_drafts
        group_drafts = await group_drafts_loader.load(group_name)
        group_drafts_titles = [draft["title"] for draft in group_drafts]
        if vuln_info["definitive_name"] in group_drafts_titles:
            target_finding = next(
                draft
                for draft in group_drafts
                if draft["title"] == vuln_info["definitive_name"]
            )

    if not target_finding:
        print(
            f'  --- {vuln_info["vuln_uuid"]}, '
            f'finding/draft "{vuln_info["definitive_name"]}" NOT found'
        )
        return False

    vuln = await vulns_dal.get(vuln_info["vuln_uuid"])
    if len(vuln) < 0:
        print(f'   --- ERROR: {vuln_info["vuln_uuid"]} NOT found')
        return False
    new_vuln = vuln[0]
    new_vuln["finding_id"] = target_finding["id"]

    success = False
    if PROD:
        # Create new one
        success = await vulns_dal.create(new_vuln)
        print(
            f'   --- {new_vuln["finding_id"]}, '
            f'vuln {new_vuln["UUID"]} created: {success}'
        )
        # Delete old one
        if success:
            success = await vulns_dal.delete(
                vuln_info["vuln_uuid"], vuln_info["finding_id"]
            )
            print(
                f'   --- {vuln_info["finding_id"]}, '
                f'vuln {vuln_info["vuln_uuid"]} deleted: {success}'
            )
    else:
        print(
            f'   === target_finding: {new_vuln["finding_id"]}, '
            f'new_vuln {new_vuln["UUID"]}'
        )
        return True

    return success


async def main() -> None:
    # Read file with deletion info
    with open("0119.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        vulns_to_move = [
            {
                "group_name": row[0],
                "finding_id": row[1],
                "finding_name": row[2],
                "vuln_uuid": row[3],
                "definitive_name": row[4],
            }
            for row in reader
            if "group" not in row[0]
        ]
    print(f"    === vulns to move: {len(vulns_to_move)}")
    print(f"    === sample: {vulns_to_move[:1]}")

    context: Dataloaders = get_new_context()
    success = all(
        await collect(process_vuln(context, vuln) for vuln in vulns_to_move)
    )

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
