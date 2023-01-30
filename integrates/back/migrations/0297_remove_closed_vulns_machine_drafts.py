# pylint: disable=invalid-name,too-many-function-args
# type: ignore
"""
Deletes all closed vulnerabilities inside Machine drafts

Execution Time:    2022-10-12 at 00:31:22 UTC
Finalization Time: 2022-10-12 at 00:41:40 UTC
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
    VulnerabilityStateStatus,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time
from vulnerabilities.domain import (
    remove_vulnerability,
)


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_drafts = await loaders.group_drafts.load_many(list(groups))
    total_groups: int = len(groups)
    for idx, (group, drafts) in enumerate(zip(groups, groups_drafts)):
        print(f"Processing {group} {idx+1}/{total_groups}...")
        machine_drafts = [
            draft for draft in drafts if draft.state.source == Source.MACHINE
        ]
        drafts_vulns = await loaders.finding_vulnerabilities.load_many_chained(
            [draft.id for draft in machine_drafts]
        )
        vulns_to_delete = [
            (
                vuln.id,
                vuln.finding_id,
                vuln.where,
                vuln.specific,
                vuln.state.status.value,
            )
            for vuln in drafts_vulns
            if vuln.state.status == VulnerabilityStateStatus.SAFE
        ]
        if vulns_to_delete:
            print("\t" + f"Deleting {len(vulns_to_delete)} vulnerabilities...")
        await collect(
            (
                remove_vulnerability(
                    loaders,
                    vuln[1],
                    vuln[0],
                    StateRemovalJustification.REPORTING_ERROR,
                    "acuberos@fluidattacks.com",
                    Source.ASM,
                    True,
                )
                for vuln in vulns_to_delete
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
