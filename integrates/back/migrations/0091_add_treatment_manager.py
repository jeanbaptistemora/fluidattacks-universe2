#  pylint: disable=invalid-name
# Add treatment manager to vulns if manager is not assigned, but the user
# field exists
#   https://gitlab.com/fluidattacks/product/-/issues/421
#
# Execution Time:    2021-06-21 at 16:21:57 UTC-05
# Finalization Time: 2021-06-21 at 17:53:31 UTC-05

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    get_new_context,
)
from findings import (
    domain as findings_domain,
)
from groups.dal import (
    get_active_groups,
)
import time
from typing import (
    Any,
    cast,
    Dict,
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = True


async def update_vuln_treatment_manager(vuln: VulnerabilityType) -> bool:
    historic_treatment = cast(
        List[Dict[str, str]], vuln.get("historic_treatment", [])
    )
    historic_treatment[-1]["treatment_manager"] = historic_treatment[-1][
        "user"
    ]
    if PROD:  # pylint: disable=no-else-return
        return await vulns_dal.update(
            str(vuln.get("finding_id", "")),
            str(vuln.get("UUID", "")),
            {"historic_treatment": historic_treatment},
        )
    else:
        print(
            f'finding_id: {vuln["finding_id"]}, UUID: {vuln["UUID"]}, '
            f"new historic treatment: {historic_treatment}"
        )

    return False


async def process_group_vulns(context: Any, group: str) -> None:
    group_findings_loader = context.group_findings
    findings = await group_findings_loader.load(group)
    are_findings_valid = await collect(
        findings_domain.validate_finding(str(finding["finding_id"]))
        for finding in findings
    )
    valid_findings = [
        finding
        for finding, is_finding_valid in zip(findings, are_findings_valid)
        if is_finding_valid
    ]

    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load_many_chained(
        [str(finding["finding_id"]) for finding in valid_findings]
    )
    if vulns:
        no_treatment_manager_vulns = [
            vuln
            for vuln in vulns
            if not vuln["historic_treatment"][-1].get("treatment_manager", "")
            if vuln["historic_treatment"][-1].get("user", "")
        ]

        if no_treatment_manager_vulns:
            vuln_len = len(no_treatment_manager_vulns)
            print(f"Vulns to update in group {group}, qty {vuln_len}")
            await collect(
                update_vuln_treatment_manager(vuln)
                for vuln in no_treatment_manager_vulns
            )
        else:
            print(f"No vulns to update in group {group}")


async def main() -> None:
    context = get_new_context()
    groups = await get_active_groups()
    print("groups to check: ", str(groups))

    await collect(process_group_vulns(context, group) for group in groups)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
