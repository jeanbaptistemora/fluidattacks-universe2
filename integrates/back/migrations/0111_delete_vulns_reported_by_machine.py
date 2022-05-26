# pylint: disable=invalid-name
"""
This migration aims to delete all vulns repoted by skims/machine from
July 21st to date.

All affected findings will be checked: if a finding has no vulns, it will
be deleted

Execution Time:     2021-07-29 at 14:01:08 UTC-05
Finalization Time:  2021-07-29 at 14:26:43 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from findings import (
    dal as findings_dal,
)
from groups.dal import (  # pylint: disable=import-error
    get_active_groups,
)
import time
from typing import (
    Any,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = True


async def process_finding(context: Any, finding_id: str) -> bool:
    success = False

    finding_vulns_loader = context.finding_vulns_all
    vulns = await finding_vulns_loader.load(finding_id)

    if len(vulns) == 0:
        return True

    # Filter vulns reported by machine (aka skims)
    vulns_machine = [
        vuln["id"]
        for vuln in vulns
        if str(vuln["source"]).lower() == "machine"
        and vuln["historic_state"][0]["date"] > "2021-07-21 00:00:00"
    ]

    if len(vulns_machine) > 0:
        print(
            f"   === finding: {finding_id}, "
            f"vulns by machine ({len(vulns_machine)}): {vulns_machine}"
        )
    else:
        return True

    if len(vulns) == len(vulns_machine):
        print(f"   >>> finding to be deleted: {finding_id}")

    if PROD:
        success = all(
            await collect(
                vulns_dal.delete(
                    vuln_uuid,
                    finding_id,
                )
                for vuln_uuid in vulns_machine
            )
        )
        if success and len(vulns) == len(vulns_machine):
            success = await findings_dal.delete(finding_id)
        if not success:
            print(f"   === ERROR with finding: {finding_id}")

    return success


async def process_group(context: Any, group_name: str) -> bool:
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group_name)
    return all(
        await collect(
            process_finding(
                context,
                str(finding["finding_id"]),
            )
            for finding in findings
        )
    )


async def main() -> None:
    context = get_new_context()
    groups = sorted(await get_active_groups())
    print(f"   === groups: {len(groups)}:\n{groups}")

    success = all(
        await collect(
            process_group(
                context,
                group,
            )
            for group in groups
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
