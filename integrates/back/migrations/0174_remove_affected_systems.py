# pylint: disable=invalid-name
"""
Remove affected_systems field from findings in DynamoDB.

This is a second attempt on this migration, processing vulns by group, not
by performing a scan operation on the whole table.
See: migrations/0167_remove_affected_systems.py

Removed and masked findings are left out as they will be migrated to redshift,
effectively removing the field in the process.
See: https://gitlab.com/fluidattacks/product/-/issues/5690

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model import (
    TABLE,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
import time
from typing import (
    List,
)


async def process_finding(
    *,
    finding: Item,
) -> None:
    await operations.update_item(
        item={"affected_systems": None},
        key=PrimaryKey(
            partition_key=finding["pk"],
            sort_key=finding["sk"],
        ),
        table=TABLE,
    )
    print(f'pk: {finding["pk"]}')


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=10,
)
async def process_group(
    *,
    group_name: str,
    progress: float,
) -> None:
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_metadata"],),
        filter_expression=Attr("affected_systems").exists(),
        index=index,
        table=TABLE,
    )
    group_findings: List[Item] = response.items
    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=64,
    )
    print(
        f"Group updated: {group_name}. "
        f"Findings processed: {len(group_findings)}. "
        f"Progress: {round(progress, 4)}"
    )


async def main() -> None:
    group_names = sorted(await groups_dal.get_active_groups())
    active_groups_len = len(group_names)
    print(f"Groups to process: {len(group_names)}")
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / active_groups_len,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=16,
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
