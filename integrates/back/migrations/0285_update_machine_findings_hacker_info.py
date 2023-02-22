# pylint: disable=invalid-name
"""
Update all machine findings so the hacker email is machine@fluidattacks.com

Execution Time:    2022-09-22 at 01:30:15 UTC
Finalization Time: 2022-09-22 at 01:39:00 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
    FindingMetadataToUpdate,
)
from db_model.findings.update import (
    update_metadata,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_group_names(loaders=loaders)
    for group in groups:
        print(f"Processing group {group}")
        findings = await loaders.group_drafts_and_findings.load(group)
        findings_to_update: list[Finding] = [
            fin
            for fin in findings
            if (
                fin.state.source == Source.MACHINE
                and fin.hacker_email != "machine@fluidattacks.com"
            )
        ]
        if findings_to_update:
            print("\t" + f"{len(findings_to_update)} findings will be updated")
            await collect(
                (
                    update_metadata(
                        group_name=group,
                        finding_id=finding.id,
                        metadata=FindingMetadataToUpdate(
                            hacker_email="machine@fluidattacks.com",
                        ),
                    )
                    for finding in findings_to_update
                ),
                workers=15,
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
