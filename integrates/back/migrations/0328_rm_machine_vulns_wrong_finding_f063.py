# pylint: disable=invalid-name
"""
Deletes all vulnerabilities reported by Machine
for method JS_PATH_TRAVERSAL and TS_PATH_TRAVERSAL of Finding 063,
because the logic was incorrect and some of them were false positives.
Executes F063 for the groups that had vulns deleted to confirm.

Execution Time:    2022-12-01 at 15:37:49 UTC
Finalization Time: 2022-12-01 at 15:42:57 UTC
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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateJustification,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain import (
    remove_finding,
)
from machine.jobs import (
    queue_job_new,
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
    findings_063 = [
        finding for finding in findings if finding.title.startswith("063")
    ]
    findings_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in findings_063]
    )
    total_findings = len(findings_063)
    groups_with_issues = set()
    for idx, (finding, vulns) in enumerate(zip(findings_063, findings_vulns)):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name} ({idx+1}/{total_findings})..."
        )
        wrong_vulns = [
            vuln
            for vuln in vulns
            if (
                vuln.state.source == Source.MACHINE
                and vuln.skims_method is not None
                and vuln.skims_method.endswith("insecure_path_traversal")
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
                            VulnerabilityStateJustification.REPORTING_ERROR,
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
    await collect(
        (
            queue_job_new(group, loaders, ["F063"])
            for group in groups_with_issues
        ),
        workers=15,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
