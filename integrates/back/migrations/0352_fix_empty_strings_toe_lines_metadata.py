# pylint: disable=invalid-name
"""
Refresh toe lines metadata and state when an empty string is in an
attribute that would hold a date. These empty strings are causing an
indexation error in opensearch. The attribute will be removed instead.

Execution Time:    2023-01-16 at 16:27:41 UTC
Finalization Time: 2023-01-16 at 19:33:17 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def get_toe_lines_by_group(
    group_name: str,
) -> tuple[Item, ...]:
    facet = TABLE.facets["toe_lines_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"group_name": group_name},
    )
    index = None
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#FILENAME", "")
            )
        ),
        facets=(facet,),
        index=index,
        table=TABLE,
    )

    return response.items


async def process_toe_lines_item(item: Item) -> None:
    attacked_at = item.get("attacked_at")
    be_present_until = item.get("be_present_until")
    first_attack_at = item.get("first_attack_at")
    if attacked_at and be_present_until and first_attack_at:
        return

    to_update: Item = {}
    if attacked_at == "":
        to_update["attacked_at"] = None
    if be_present_until == "":
        to_update["be_present_until"] = None
    if first_attack_at == "":
        to_update["first_attack_at"] = None
    if not to_update:
        return

    key_structure = TABLE.primary_key
    primary_key = PrimaryKey(
        partition_key=item[TABLE.primary_key.partition_key],
        sort_key=item[TABLE.primary_key.sort_key],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=to_update,
        key=primary_key,
        table=TABLE,
    )


async def process_group(group_name: str, progress: float) -> None:
    group_toe_lines = await get_toe_lines_by_group(group_name)
    print(
        f"Working on {group_name=}, {len(group_toe_lines)=}, "
        f"progress: {round(progress, 2)}"
    )
    if not group_toe_lines:
        return

    await collect(
        tuple(process_toe_lines_item(item) for item in group_toe_lines),
        workers=64,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
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
