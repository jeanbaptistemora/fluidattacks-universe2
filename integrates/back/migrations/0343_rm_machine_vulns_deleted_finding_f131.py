# pylint: disable=invalid-name
"""
Deletes all vulnerabilities reported by Machine
for C# method 'check_default_usehsts' of Finding 131,
because the method was not deterministic so it was removed from the queries.

Execution Time:    2022-12-28 at 17:14:15 UTC
Finalization Time: 2022-12-28 at 17:15:42 UTC
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
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain import (
    remove_finding,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time
from typing import (
    Tuple,
)
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_finding_unreliable_indicators,
)
from vulnerabilities.domain import (
    remove_vulnerability,
)


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    findings = await loaders.group_drafts_and_findings.load_many_chained(
        groups
    )
    findings_131 = [
        finding for finding in findings if finding.title.startswith("131")
    ]
    findings_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in findings_131]
    )
    total_findings = len(findings_131)
    groups_with_issues = set()
    for idx, (finding, vulns) in enumerate(zip(findings_131, findings_vulns)):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name} ({idx+1}/{total_findings})..."
        )
        wrong_vulns = [
            vuln
            for vuln in vulns
            if (
                (
                    vuln.state.source == Source.MACHINE
                    or vuln.hacker_email == "machine@fluidattacks.com"
                )
                and vuln.skims_method is not None
                and vuln.skims_method.endswith("check_default_usehsts")
            )
        ]
        if wrong_vulns:
            print("\t" + f"{len(wrong_vulns)} vulnerabilities with errors")
            groups_with_issues.add(finding.group_name)
            if len(wrong_vulns) == len(vulns):
                await remove_finding(
                    loaders,
                    "flagos@fluidattacks.com",
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
                            StateRemovalJustification.REPORTING_ERROR,
                            "flagos@fluidattacks.com",
                            True,
                        )
                        for vuln in wrong_vulns
                    ),
                    workers=15,
                )
                await update_finding_unreliable_indicators(
                    finding.id,
                    {
                        EntityAttr.closed_vulnerabilities,
                        EntityAttr.newest_vulnerability_report_date,
                        EntityAttr.oldest_open_vulnerability_report_date,
                        EntityAttr.oldest_vulnerability_report_date,
                        EntityAttr.open_vulnerabilities,
                        EntityAttr.status,
                        EntityAttr.where,
                        EntityAttr.treatment_summary,
                        EntityAttr.verification_summary,
                    },
                )
    print(groups_with_issues)


if __name__ == "__main__":
    start_time = time.strftime("Execution Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(f"{start_time}")
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{start_time}\n{finalization_time}")
