# pylint: disable=invalid-name
"""
Refresh vulnerabilities unreliable_indicators when an empty string is in an
attribute that would hold a date. These empty strings are causing an
indexation error in opensearch. The attribute will be removed instead.

Execution Time:    2023-01-12 at 21:37:11 UTC
Finalization Time: 2023-01-13 at 05:16:42 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityUnreliableIndicatorsToUpdate,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def process_vulnerability(vulnerability: Vulnerability) -> None:
    indicators = vulnerability.unreliable_indicators
    if not (
        indicators.unreliable_closing_date
        and indicators.unreliable_last_reattack_date
        and indicators.unreliable_last_requested_reattack_date
    ):
        await vulns_model.update_unreliable_indicators(
            current_value=vulnerability,
            indicators=VulnerabilityUnreliableIndicatorsToUpdate(
                clean_unreliable_closing_date=not bool(
                    indicators.unreliable_closing_date
                ),
                clean_unreliable_last_reattack_date=not bool(
                    indicators.unreliable_last_reattack_date
                ),
                clean_unreliable_last_requested_reattack_date=not bool(
                    indicators.unreliable_last_requested_reattack_date
                ),
            ),
        )


async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    vulns = await loaders.finding_vulnerabilities_all.load(finding.id)
    await collect(
        tuple(process_vulnerability(vuln) for vuln in vulns),
        workers=16,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)

    await collect(
        tuple(process_finding(loaders, finding) for finding in group_findings),
        workers=8,
    )

    print(
        f"Processed {group_name=}, {len(group_findings)=}, "
        f"progress: {round(progress, 2)}"
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    print(f"{len(group_names)=}")

    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=1,
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
