# pylint: disable=invalid-name
"""
Move migrated attributes from the ToeLines Item into the State

TOE Lines State Standardization
Execution Time:    2023-01-20 at 21:00:45 UTC
Finalization Time: 2023-01-20 at 22:01:59 UTC

TOE Lines Check
Execution Time:
Finalization Time:

Deletion of duplicate data
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

MIGRATED_ATTRS = {
    "loc",
    "comments",
    "sorts_risk_level",
    "sorts_risk_level_date",
    "last_commit",
    "last_author",
    "has_vulnerabilities",
    "attacked_at",
    "first_attack_at",
    "be_present",
    "attacked_by",
    "attacked_lines",
    "seen_at",
    "sorts_suggestions",
    "modified_date",
}
MIGRATE = False


def check_item_state_shape(item: Item, state_item: Item) -> None:
    if lacking_attrs := (MIGRATED_ATTRS & item.keys()) - state_item.keys():
        print(f"Found an item/state mismatch:{lacking_attrs}")
        print(f"Item: {item}")
    if any(
        attr not in state_item for attr in ("modified_by", "modified_date")
    ):
        print("State missing some attrs")


async def get_toe_lines_by_group(
    group_name: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#ROOT#FILENAME", "")
            )
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        index=None,
        table=TABLE,
    )

    return response.items


async def delete_duplicate_data(item: Item) -> None:
    to_delete: Item = {
        key: None for key in (MIGRATED_ATTRS - {"modified_date"})
    }

    key_structure = TABLE.primary_key
    primary_key = PrimaryKey(
        partition_key=item[TABLE.primary_key.partition_key],
        sort_key=item[TABLE.primary_key.sort_key],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=to_delete,
        key=primary_key,
        table=TABLE,
    )


async def process_toe_lines_item(item: Item) -> None:
    state_item: Item = dict(item.get("state", {}))
    keys_to_update = (MIGRATED_ATTRS & item.keys()) - state_item.keys()

    if not keys_to_update:
        return
    to_update: Item = (
        {key: item[key] for key in keys_to_update}
        | {
            "modified_by": item["attacked_by"]
            if item.get("attacked_by")
            else "machine@fluidattacks.com"
        }
        | state_item
    )

    key_structure = TABLE.primary_key
    primary_key = PrimaryKey(
        partition_key=item[TABLE.primary_key.partition_key],
        sort_key=item[TABLE.primary_key.sort_key],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item={"state": to_update},
        key=primary_key,
        table=TABLE,
    )


async def process_group(group_name: str, progress: float) -> None:
    group_toe_lines = await get_toe_lines_by_group(group_name)
    print(
        f"Working on {group_name}, {len(group_toe_lines)}, "
        f"progress: {round(progress, 2)}"
    )
    if not group_toe_lines:
        return

    if MIGRATE:
        await collect(
            tuple(process_toe_lines_item(item) for item in group_toe_lines),
            workers=64,
        )
    else:
        for item in group_toe_lines:
            check_item_state_shape(item, item["state"])


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
