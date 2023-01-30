# pylint: disable=invalid-name
"""
Deletes all findings and vulnerabilities reported by Machine
for type `419. Traceability Loss - Kubernetes`
since the logic was incorrect and all of them were false positives.
Findings that had squad vulnerabilities were not deleted entirely,
just the Machine vulnerabilities.

Execution Time:    2022-11-09 at 20:47:06 UTC
Finalization Time: 2022-11-09 at 20:57:27 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from findings.domain import (
    remove_finding,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time
from typing import (
    List,
)
from vulnerabilities.domain import (
    remove_vulnerability,
)


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_findings = (
        await loaders.group_drafts_and_findings.load_many_chained(list(groups))
    )

    f419_findings: List[Finding] = [
        finding
        for finding in groups_findings
        if finding.state.status
        not in [FindingStateStatus.DELETED, FindingStateStatus.MASKED]
        and finding.title.startswith("419")
    ]
    f419_vulns = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in f419_findings]
    )
    total_findings: int = len(f419_findings)
    for idx, (finding, vulns) in enumerate(zip(f419_findings, f419_vulns)):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name}({idx+1}/{total_findings})..."
        )
        machine_vulns = [
            vuln for vuln in vulns if vuln.state.source == Source.MACHINE
        ]
        if machine_vulns:
            print("\t" + f"Deleting {len(machine_vulns)}...")
            if len(machine_vulns) == len(vulns):
                await remove_finding(
                    loaders,
                    "acuberos@fluidattacks.com",
                    finding.id,
                    StateRemovalJustification.REPORTING_ERROR,
                    Source.ASM,
                )
            else:
                await collect(
                    (
                        remove_vulnerability(
                            loaders,
                            finding.id,
                            vuln.id,
                            VulnerabilityStateReason.REPORTING_ERROR,
                            "acuberos@fluidattacks.com",
                            True,
                        )
                        for vuln in machine_vulns
                    ),
                    workers=20,
                )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
