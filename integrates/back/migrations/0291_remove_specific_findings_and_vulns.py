# pylint: disable=invalid-name
"""
Remove unwanted findings and their vulns for specific orgs.

Execution Time:    2022-09-30 at 15:27:54 UTC
Finalization Time: 2022-09-30 at 16:10:05 UTC
"""

from aioextensions import (
    collect,
    run,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from findings import (
    domain as findings_domain,
)
from newutils import (
    groups as groups_utils,
)
import time
from typing import (
    Any,
)

FINDING_TITLES_TO_DELETE: list[str] = [
    "049. Inappropriate coding practices - Unused variables",
    "074. Commented-out code",
    "139. Use of deprecated components",
    "303. Inappropriate coding practices - Initialization",
]
PROD: bool = True


async def _process_group(
    loaders: Dataloaders, group_name: str, org_name: str
) -> list[dict[str, Any]]:
    print(f"Working on {org_name} : {group_name}...")
    findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    filtered = tuple(
        finding
        for finding in findings
        if finding.title in FINDING_TITLES_TO_DELETE
    )

    if PROD:
        await collect(
            tuple(
                findings_domain.remove_finding(
                    loaders=loaders,
                    email="integrates@fluidattacks.com",
                    finding_id=finding.id,
                    justification=StateRemovalJustification.NOT_REQUIRED,
                    source=Source.ASM,
                )
                for finding in filtered
            ),
            workers=16,
        )

    return [
        {
            "organization": org_name,
            "group": finding.group_name,
            "finding_id": finding.id,
            "title": finding.title,
            "status": finding.state.status.value,
            "vulns_qty": len(
                await loaders.finding_vulnerabilities_all.load(finding.id)
            ),
        }
        for finding in filtered
    ]


async def _process_organization(
    loaders: Dataloaders, org_name: str
) -> list[dict[str, Any]]:
    print(f"Working on {org_name=}...")
    organization: Organization = await loaders.organization.load(org_name)
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    active_groups = groups_utils.filter_active_groups(tuple(org_groups))
    print(f"{org_name=}, {len(active_groups)=}")

    results: list[dict[str, Any]] = []
    for group in active_groups:
        results.extend(
            await _process_group(
                loaders=loaders,
                group_name=group.name,
                org_name=organization.name,
            )
        )

    return results


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    org_names_to_process: list[str] = []  # Masked

    results: list[dict[str, Any]] = []
    for org_name in org_names_to_process:
        results.extend(await _process_organization(loaders, org_name))

    csv_columns = [
        "organization",
        "group",
        "finding_id",
        "title",
        "status",
        "vulns_qty",
    ]
    csv_file = "0291.csv"
    try:
        with open(csv_file, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            for data in results:
                writer.writerow(data)
    except IOError:
        print("   === I/O error")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
