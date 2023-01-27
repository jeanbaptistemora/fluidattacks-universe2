# pylint: disable=invalid-name
"""
Move migrated attributes from the ToeInputs Item into the State

TOE Inputs State Standardization
Execution Time:    2023-01-27 at 20:34:35 UTC
Finalization Time: 2023-01-27 at 20:46:02 UTC

TOE Inputs Check
Execution Time:    2023-01-27 at 20:47:00 UTC
Finalization Time: 2023-01-27 at 20:50:10 UTC

Deletion of duplicate data
Execution Time:    2023-01-27 at 23:03:37 UTC
Finalization Time: 2023-01-27 at 23:14:08 UTC
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
from db_model.toe_inputs.utils import (
    format_toe_input,
)
from db_model.utils import (
    serialize,
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
from newutils.datetime import (
    get_iso_date,
)
from organizations import (
    domain as orgs_domain,
)
import simplejson as json
import time

MIGRATED_ATTRS = {
    "attacked_at",
    "attacked_by",
    "be_present",
    "be_present_until",
    "first_attack_at",
    "has_vulnerabilities",
    "seen_at",
    "seen_first_time_by",
    "unreliable_root_id",
}
MIGRATE = False
DELETE = False
MISSING_GROUPS: set[str] = set()


def check_item_state_shape(state_item: Item) -> bool:
    return {"modified_by", "modified_date"} >= state_item.keys()


async def get_toe_inputs_by_group(
    group_name: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_input_metadata"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#ROOT#COMPONENT#ENTRYPOINT", "")
            )
        ),
        facets=(TABLE.facets["toe_input_metadata"],),
        index=None,
        table=TABLE,
    )

    return response.items


async def delete_duplicate_data(item: Item) -> None:
    to_delete: Item = {key: None for key in (MIGRATED_ATTRS & item.keys())}
    if check_item_state_shape(item["state"]) or not to_delete:
        return

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


async def process_toe_inputs_item(group_name: str, item: Item) -> None:
    toe_input = format_toe_input(group_name=group_name, item=item)
    state_item: Item = json.loads(
        json.dumps(toe_input.state, default=serialize)
    )

    if state_item.get("modified_date") is None:
        state_item["modified_date"] = get_iso_date()
    if state_item.get("modified_by") is None:
        state_item["modified_by"] = "machine@fluidattacks.com"

    if state_item == item.get("state"):
        return

    key_structure = TABLE.primary_key
    primary_key = PrimaryKey(
        partition_key=item[TABLE.primary_key.partition_key],
        sort_key=item[TABLE.primary_key.sort_key],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item={"state": state_item},
        key=primary_key,
        table=TABLE,
    )


async def process_group(group_name: str, progress: float) -> None:
    group_toe_inputs = await get_toe_inputs_by_group(group_name)
    print(
        f"Working on {group_name}, {len(group_toe_inputs)}, "
        f"progress: {round(progress, 2)}"
    )
    if not group_toe_inputs:
        return

    if MIGRATE:
        await collect(
            tuple(
                process_toe_inputs_item(group_name, item)
                for item in group_toe_inputs
            ),
            workers=64,
        )
    elif DELETE:
        await collect(
            tuple(delete_duplicate_data(item) for item in group_toe_inputs),
            workers=64,
        )
    else:
        for item in group_toe_inputs:
            if check_item_state_shape(item["state"]):
                print(f"Found mismatch in {group_name}")
                MISSING_GROUPS.add(group_name)
                return


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
    if not MIGRATE:
        print(MISSING_GROUPS)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
