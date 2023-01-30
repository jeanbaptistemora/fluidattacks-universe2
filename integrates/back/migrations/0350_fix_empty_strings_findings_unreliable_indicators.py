# pylint: disable=invalid-name
"""
Refresh findings unreliable_indicators when an empty string is in an
attribute that would hold a date. These empty strings are causing an
indexation error in opensearch. The attribute will be removed instead.

Execution Time:    2023-01-13 at 14:25:02 UTC
Finalization Time: 2023-01-13 at 15:17:35 UTC
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
    findings as findings_model,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicatorsToUpdate,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def process_finding(finding: Finding) -> None:
    indicators = finding.unreliable_indicators
    if (
        indicators.unreliable_newest_vulnerability_report_date
        and indicators.unreliable_oldest_open_vulnerability_report_date
        and indicators.unreliable_oldest_vulnerability_report_date
    ):
        return

    await findings_model.update_unreliable_indicators(
        current_value=indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=FindingUnreliableIndicatorsToUpdate(
            clean_unreliable_newest_vulnerability_report_date=not bool(
                indicators.unreliable_newest_vulnerability_report_date
            ),
            clean_unreliable_oldest_open_vulnerability_report_date=not bool(
                indicators.unreliable_oldest_open_vulnerability_report_date
            ),
            clean_unreliable_oldest_vulnerability_report_date=not bool(
                indicators.unreliable_oldest_vulnerability_report_date
            ),
        ),
    )
    print(f"Finding updated {finding.id=}")


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(process_finding(finding) for finding in group_findings),
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
