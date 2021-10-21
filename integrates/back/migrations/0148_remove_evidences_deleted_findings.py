# pylint: disable=invalid-name
"""
This migration aims to remove evidences for deleted findings.

Execution Time:     2021-10-20 at 16:28:30 UTC
Finalization Time:  2021-10-20 at 19:10:07 UTC
"""

from aioextensions import (
    collect,
    run,
)
from context import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from s3.operations import (
    list_files,
    remove_file,
)
import time
from typing import (
    List,
    Tuple,
)

PROD: bool = True


async def _process_evidence(full_name: str) -> None:
    await remove_file(EVIDENCES_BUCKET, full_name)
    print(f"Removed: {full_name}")


async def _process_finding(finding: Finding) -> None:
    evidences: List[str] = await list_files(
        EVIDENCES_BUCKET, f"{finding.group_name}/{finding.id}/"
    )

    if not evidences:
        return

    if PROD:
        await collect(_process_evidence(full_name) for full_name in evidences)
    else:
        print(f"Found evidences: {evidences}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()

    group_names = await groups_domain.get_alive_group_names()
    group_names = sorted(
        [
            group
            for group in group_names
            if group
            not in {
                "unittesting",
                "continuoustest",
                "detailedtest",
                "napervilletest",
            }
        ]
    )
    print(f"Groups to check: {len(group_names)}")

    findings: Tuple[Finding, ...] = tuple(
        chain.from_iterable(
            await loaders.group_removed_findings.load_many(group_names)
        )
    )
    print(f"Deleted findings to check: {len(findings)}")

    await collect(_process_finding(finding) for finding in findings)

    print("Done")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
