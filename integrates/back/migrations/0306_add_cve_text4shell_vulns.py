# pylint: disable=invalid-name
# type: ignore
"""
Update existing Text4Shell vulnerabilities
that were reported with the ID of the Github Advisory
to include the CVE ID.

Execution Time: 2022-10-25 at 21:00:58 UTC
Finalization Time: 2022-10-25 at 21:04:40 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_findings = await loaders.group_findings.load_many_chained(
        list(groups)
    )
    sca_findings: list[Finding] = [
        finding
        for finding in groups_findings
        if any(finding.title.startswith(code) for code in ["011", "393"])
    ]
    sca_vulns = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in sca_findings]
    )

    gh_advisory = "GHSA-599f-7c49-w659"
    for finding, vulns in zip(sca_findings, sca_vulns):
        text4shell_vulns = [
            vuln for vuln in vulns if f"[{gh_advisory}]" in vuln.where
        ]

        if text4shell_vulns:
            print(
                f"Updating {len(text4shell_vulns)} vulnerabilities "
                f"in finding {finding.title} in group {finding.group_name}"
            )
            print(
                "\t" + "\n\t".join([vuln.where for vuln in text4shell_vulns])
            )
            await collect(
                (
                    update_metadata(
                        finding_id=finding.id,
                        metadata=VulnerabilityMetadataToUpdate(
                            where=vuln.where.replace(
                                f"[{gh_advisory}]",
                                f"[CVE-2022-42889, {gh_advisory}]",
                            )
                        ),
                        vulnerability_id=vuln.id,
                    )
                    for vuln in text4shell_vulns
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
