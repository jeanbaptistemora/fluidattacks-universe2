# pylint: disable=invalid-name
"""
Remove evidences in S3 that belong to no current draft or finding,
in active groups.
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from organizations import (
    domain as orgs_domain,
)
from s3 import (
    operations as s3_ops,
)
import time


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    evidence_file_names = await s3_ops.list_files(f"evidences/{group_name}")
    if not evidence_file_names:
        return

    group_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    finding_ids = [finding.id for finding in group_findings]

    evidences_without_finding = [
        evidence
        for evidence in evidence_file_names
        if evidence.split("/")[2] not in finding_ids
    ]
    if not evidences_without_finding:
        return

    await collect(
        tuple(
            s3_ops.remove_file(name=evidence)
            for evidence in evidences_without_finding
        ),
        workers=4,
    )

    print(f"Processed {group_name=}, {len(evidences_without_finding)=}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    print(f"{len(group_names)=}")

    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
            )
            for group_name in group_names
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
