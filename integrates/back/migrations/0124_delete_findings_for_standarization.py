# pylint: disable=invalid-name
"""
This migration aims to delete findings without vulns, in order to continue with
the findings type standarization effort.

The finding ids to be checked, and possibly deleted, are taken from previous
migrations.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-19 at 13:16:59 UTC-05
Finalization Time: 2021-08-19 at 13:17:01 UTC-05

Execution Time:    2021-08-20 at 21:24:33 UTC-05
Finalization Time: 2021-08-20 at 21:44:53 UTC-05

Execution Time:    2021-08-23 at 10:48:48 UTC-05
Finalization Time: 2021-08-23 at 11:55:16 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_types import (
    Finding as FindingType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings import (
    dal as findings_dal,
    domain as findings_domain,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
import time
from typing import (
    Dict,
    List,
)

PROD: bool = True


async def process_finding(context: Dataloaders, finding_id: str) -> bool:

    finding: Dict[str, FindingType] = await findings_dal.get_finding(
        finding_id
    )
    if not finding:
        print(f"   --- ERROR finding {finding_id} NOT found")
        return False

    finding_vulns_nzr_loader = context.finding_vulns_nzr
    vulns_nzr = await finding_vulns_nzr_loader.load(finding_id)
    has_vulns = [
        vuln for vuln in vulns_nzr if vulns_utils.filter_deleted_status(vuln)
    ]
    if has_vulns:
        print(f"   --- WARNING: finding {finding_id} has vulns. NO deletion")
        return False

    success = False
    if PROD:
        finding_files: List[Dict[str, str]] = finding.get("files", [])
        if finding_files:
            success = all(
                await collect(
                    findings_domain.remove_evidence(file["name"], finding_id)
                    for file in finding_files
                )
            )
            print(f"   === finding {finding_id} evidences deleted: {success}")
        else:
            success = True
        if success:
            success = await findings_dal.delete(finding_id)
            print(f"   === finding {finding_id} deleted: {success}")
    else:
        print(f"   === finding {finding_id} could be DELETED")

    return success


async def main() -> None:
    with open("0119.csv", mode="r") as f:
        reader = csv.reader(f)
        finding_ids = set([row[1] for row in reader if "group" not in row[0]])
    print(f"   === finding ids ({len(finding_ids)}): {finding_ids}")

    context: Dataloaders = get_new_context()
    success = all(
        await collect(
            [
                process_finding(context, finding_id)
                for finding_id in finding_ids
            ]
        )
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
