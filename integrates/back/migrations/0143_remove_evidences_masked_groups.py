# pylint: disable=invalid-name
"""
This migration aims to remove evidences for deleted groups.
When the deletion occurs, the findings should be masked and the evidences
removed from S3.

Execution Time:    2021-10-08 at 16:25:00 UTC
Finalization Time: 2021-10-08 at 18:35:00 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
from s3.operations import (
    list_files,
    remove_file,
)
import time

PROD: bool = True


async def _process_evidence(full_name: str) -> None:
    await remove_file(full_name)
    print(f"Removed: {full_name}")


async def main() -> None:
    filtering_exp = Attr("project_status").eq("DELETED") | Attr(
        "project_status"
    ).eq("FINISHED")
    masked_groups = sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )
    print(f"Masked groups: {len(masked_groups)}")

    groups_evidences = tuple(
        chain.from_iterable(
            await collect(list_files(f"{group}/") for group in masked_groups)
        )
    )
    print(f"Evidences masked groups: {len(groups_evidences)}")
    print(f"Sample: {groups_evidences[:3]}")

    if PROD:
        await collect(
            _process_evidence(evidence) for evidence in groups_evidences
        )

    print(f"Evidences masked groups: {len(groups_evidences)}")
    print("Done")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
