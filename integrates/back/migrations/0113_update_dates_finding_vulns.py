# pylint: disable=invalid-name
"""
This migration aims to validate if the discovery date in all findings
is the same, or older, than the date of creation for its vulns.

https://gitlab.com/fluidattacks/product/-/issues/4271

Execution Time:     2021-08-02 at 06:43:08 UTC-05
Finalization Time:  2021-08-02 at 08:05:06 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Finding as FindingType,
)
from dataloaders import (
    get_new_context,
)
from groups.dal import (
    get_active_groups,
)
from newutils import (
    findings as findings_utils,
)
import time
from typing import (
    Any,
    Dict,
)
from vulnerabilities import (
    domain as vulns_domain,
)

PROD: bool = True


async def process_finding(
    context: Any,
    finding: Dict[str, FindingType],
) -> bool:
    success = False
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding["finding_id"])

    if len(vulns) == 0:
        return True

    release_date = findings_utils.get_approval_date(finding)
    new_vulns = [
        vuln
        for vuln in vulns
        if vuln["historic_treatment"][-1]["treatment"] == "NEW"
        and release_date > vuln["historic_treatment"][-1]["date"]
    ]

    uuids = [vuln["id"] for vuln in new_vulns]
    if len(new_vulns) > 0:
        print(
            f'   >>> finding: {finding["finding_id"]}, release: {release_date}'
            f", new vulns ({len(new_vulns)}): {uuids}"
        )
    else:
        return True

    if PROD:
        success = all(
            await collect(
                vulns_domain.update_historics_dates_old(
                    finding["finding_id"],
                    vuln,
                    release_date,
                )
                for vuln in new_vulns
            )
        )

    return success


async def process_group(context: Any, group_name: str) -> bool:
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group_name)
    return all(
        await collect(
            process_finding(
                context,
                finding,
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
