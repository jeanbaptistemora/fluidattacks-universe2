# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration fix those vuln deletion dates that have a lot of time difference
with the finding deletion date. Those vuln deletion dates were introduced with
the migration 0055_add_deleted_status.

Execution Time:    2021-01-14 at 09:59:47 UTC-05
Finalization Time: 2021-01-15 at 08:00:00 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import copy
from custom_types import (
    Finding as FindingType,
    Vulnerability as VulnerabilityType,
)
from datetime import (
    datetime,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
from pprint import (
    pprint,
)
from typing import (
    Dict,
)
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)


async def fix_vuln_deletion_dates(
    vuln: VulnerabilityType, finding_id: str, finding_delation_date: datetime
) -> bool:
    success = True
    old_historic_state = vuln.get("historic_state", [])
    historic_state = copy.deepcopy(old_historic_state)
    last_state_info = historic_state[-1]
    if last_state_info["state"] == "DELETED":
        vuln_deletion_date = datetime_utils.get_from_str(
            last_state_info["date"]
        )
        if (vuln_deletion_date - finding_delation_date).days > 1:
            finding_delation_date_str = datetime_utils.get_as_str(
                finding_delation_date
            )
            last_state_info["date"] = finding_delation_date_str
            success = await vulns_dal.update(
                finding_id, vuln["UUID"], {"historic_state": historic_state}
            )
            print(f"finding_id = {finding_id}")
            print(f"finding_delation_date_str = {finding_delation_date_str}")
            print(f'vuln_id = {vuln["UUID"]}')
            print("old_historic_state =")
            pprint(old_historic_state)
            print("historic_state =")
            pprint(historic_state)

    return success


async def fix_vuln_deletion_dates_for_finding(
    finding: Dict[str, FindingType],
) -> bool:
    success = True
    finding_id: str = str(finding["finding_id"])
    historic_state = finding.get("historic_state", [])
    last_state_info = historic_state[-1]
    if last_state_info["state"] == "DELETED":
        finding_delation_date = datetime_utils.get_from_str(
            last_state_info["date"]
        )
        vulns = await vulns_domain.list_vulnerabilities_async(
            [finding_id],
            include_confirmed_zero_risk=True,
            include_requested_zero_risk=True,
            should_list_deleted=True,
        )
        success = all(
            await collect(
                [
                    fix_vuln_deletion_dates(
                        vuln, finding_id, finding_delation_date
                    )
                    for vuln in vulns
                ]
            )
        )

    return success


async def fix_vuln_deletion_dates_for_group(group_name: str) -> bool:
    attrs = {"finding_id", "historic_state"}
    group_findings = await findings_domain.get_findings_by_group(
        group_name, attrs, include_deleted=True
    )
    success = all(
        await collect(
            [
                fix_vuln_deletion_dates_for_finding(finding)
                for finding in group_findings
            ]
        )
    )

    return success


async def main() -> None:
    groups = await groups_domain.get_alive_groups()
    success = all(
        await collect(
            [fix_vuln_deletion_dates_for_group(group) for group in groups],
            workers=10,
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
