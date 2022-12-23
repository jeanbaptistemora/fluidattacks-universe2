# pylint: disable=invalid-name
"""
Remove evidences in S3 that belong to deleted groups, not currently
present in db.

Execution Time:    2022-12-23 at 17:06:18 UTC
Finalization Time: 2022-12-23 at 17:10:57 UTC
"""
from aioextensions import (
    collect,
    run,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from newutils import (
    groups as groups_utils,
)
from organizations import (
    domain as orgs_domain,
)
from s3 import (
    operations as s3_ops,
)
from s3.resource import (
    get_s3_resource,
)
import time
from typing import (
    Optional,
)


async def _s3_list_files(
    name: Optional[str] = None,
    start_after: Optional[str] = "",
) -> tuple[bool, list[str]]:
    client = await get_s3_resource()
    resp = await client.list_objects_v2(
        Bucket=FI_AWS_S3_MAIN_BUCKET,
        Prefix=f"{FI_AWS_S3_PATH_PREFIX}{name}",
        StartAfter=start_after,
    )
    is_truncated: bool = resp.get("IsTruncated", False)
    keys = [
        item["Key"].replace(FI_AWS_S3_PATH_PREFIX, "")
        for item in resp.get("Contents", [])
    ]

    return (is_truncated, keys)


async def _get_group_names_to_clean(loaders: Dataloaders) -> list[str]:
    s3_evidence_file_names: list[str] = []
    is_truncated = True
    start_after = ""
    while is_truncated:
        is_truncated, results = await _s3_list_files(
            name="evidences/", start_after=start_after
        )
        s3_evidence_file_names.extend(results)
        start_after = results[-1]

    s3_evidences_group_names = set(
        key.split("/")[1]
        for key in s3_evidence_file_names
        if len(key.split("/")) > 2 and key.split("/")[1]
    )
    dynamo_active_groups = groups_utils.filter_active_groups(
        await orgs_domain.get_all_groups(loaders=loaders)
    )
    dynamo_active_group_names = set(
        group.name for group in dynamo_active_groups
    )
    s3_group_names_to_clean = sorted(
        list(s3_evidences_group_names - dynamo_active_group_names)
    )

    return s3_group_names_to_clean


async def _process_group(
    group_name: str,
    progress: float,
) -> None:
    evidence_file_names = await s3_ops.list_files(f"evidences/{group_name}")
    await collect(
        tuple(
            s3_ops.remove_file(name=evidence)
            for evidence in evidence_file_names
        ),
        workers=8,
    )
    print(
        f"Processed {group_name=}, {len(evidence_file_names)=}, "
        f"progress: {round(progress, 2)}"
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    s3_group_names_to_clean = await _get_group_names_to_clean(loaders=loaders)
    print(f"{len(s3_group_names_to_clean)=}")
    print(f"{s3_group_names_to_clean=}")

    await collect(
        tuple(
            _process_group(
                group_name=group_name,
                progress=count / len(s3_group_names_to_clean),
            )
            for count, group_name in enumerate(s3_group_names_to_clean)
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
