# pylint: disable=invalid-name
"""
Remove unwanted finding items for latest states and unreliable indicators.
This info is now in the metadata.

Execution Time:    2022-07-07 at 03:09:28 UTC
Finalization Time: 2022-07-07 at 03:18:14 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_finding(finding: Finding) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    index = TABLE.indexes["inverted_index"]
    response_index = await operations.query(
        condition_expression=(
            Key(index.primary_key.partition_key).eq(primary_key.sort_key)
            & Key(index.primary_key.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["finding_approval"],
            TABLE.facets["finding_creation"],
            TABLE.facets["finding_state"],
            TABLE.facets["finding_submission"],
            TABLE.facets["finding_unreliable_indicators"],
            TABLE.facets["finding_verification"],
        ),
        index=index,
        table=TABLE,
    )

    items = set(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response_index.items
        if item[TABLE.primary_key.partition_key] != primary_key.partition_key
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item.partition_key,
                sort_key=item.sort_key,
            )
            for item in items
        ),
        table=TABLE,
    )


async def process_group(
    *,
    group_name: str,
    loaders: Dataloaders,
    progress: float,
) -> None:
    group_findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=16,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "drafts_and_findings": len(group_findings),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_group_names = sorted(await get_all_active_group_names(loaders))
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_group_names)}},
    )

    await collect(
        tuple(
            process_group(
                group_name=group_name,
                loaders=loaders,
                progress=count / len(active_group_names),
            )
            for count, group_name in enumerate(active_group_names)
        ),
        workers=4,
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
