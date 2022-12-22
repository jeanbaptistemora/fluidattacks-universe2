# pylint: disable=invalid-name
"""
Deletes Machine drafts with zero vulnerabilities reported,
orphaned from a bug a few weeks ago

Execution Time:    2022-10-12 at 00:13:31 UTC
Finalization Time: 2022-10-12 at 00:17:52 UTC
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
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
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


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_drafts: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_drafts.load_many(groups)
    total_groups: int = len(groups)
    for idx, (group, drafts) in enumerate(zip(groups, groups_drafts)):
        print(f"Processing {group} {idx+1}/{total_groups}...")
        machine_drafts = [
            draft for draft in drafts if draft.state.source == Source.MACHINE
        ]
        drafts_vulns: Tuple[
            Tuple[Vulnerability, ...], ...
        ] = await loaders.finding_vulnerabilities.load_many(
            [draft.id for draft in machine_drafts]
        )
        drafts_to_delete = []
        for draft, vulns in zip(drafts, drafts_vulns):
            open_vulns = [
                vuln
                for vuln in vulns
                if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            ]
            if len(open_vulns) == 0:
                drafts_to_delete.append((draft.id, draft.title))
        await collect(
            (
                remove_finding(
                    loaders,
                    "acuberos@fluidattacks.com",
                    draft_id,
                    StateRemovalJustification.REPORTING_ERROR,
                    Source.ASM,
                )
                for draft_id, _ in drafts_to_delete
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
