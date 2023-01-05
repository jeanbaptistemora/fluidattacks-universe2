# pylint: disable=invalid-name
"""
Eliminate vulnerabilities reported by machine and containing false positives

Execution Time:    2022-11-22 at 18:07:39 UTC
Finalization Time: 2022-11-22 at 18:12:53 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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
    selected_findings = [
        finding
        for finding in findings
        if finding.title.startswith(("236", "332", "400"))
    ]
    findings_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in selected_findings]
    )
    total_findings = len(selected_findings)
    groups_with_issues = set()
    for idx, (finding, vulns) in enumerate(
        zip(selected_findings, findings_vulns)
    ):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name} ({idx+1}/{total_findings})..."
        )
        wrong_vulns = [
            vuln
            for vuln in vulns
            if (
                vuln.skims_method is not None
                and vuln.skims_method.endswith(
                    (
                        "json_check_https_argument",
                        "json_sourcemap_in_build",
                        "cfn_lambda_function_has_tracing_disabled",
                    )
                )
            )
        ]
        if wrong_vulns:
            print("\t" + f"{len(wrong_vulns)} vulnerabilities with errors")
            await collect(
                (
                    remove_vulnerability(
                        loaders,
                        finding.id,
                        vuln.id,
                        VulnerabilityStateReason.REPORTING_ERROR,
                        "jecheverri@fluidattacks.com",
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
            groups_with_issues.add(finding.group_name)
    print(groups_with_issues)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
