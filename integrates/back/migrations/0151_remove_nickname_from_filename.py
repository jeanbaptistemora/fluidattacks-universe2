# pylint: disable=invalid-name
"""
Remove the root nickname from the toe lines filename.

Execution Time:    2021-10-26 at 12:59:15 UTC
Finalization Time: 2021-10-26 at 16:42:20 UTC
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
from db_model.roots.types import (
    GitRootItem,
    RootItem,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups import (
    domain as groups_domain,
)
from more_itertools.more import (
    chunked,
)
import time
from typing import (
    Dict,
    Tuple,
)


def format_sk(nicknames: Dict[str, str], sk: str) -> str:
    sk.split("#", 4)
    sort_key_items = sk.split("#", 4)
    root_id = sort_key_items[2]
    filename = sort_key_items.pop()
    if not nicknames.get(root_id):
        return sk
    new_filename = filename.replace(f"{nicknames[root_id]}/", "")
    return "#".join([*sort_key_items, new_filename])


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=5,
)
async def remove_nicknames(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    print("Group", group_name)
    print("Progress", progress)
    key_structure = TABLE.primary_key
    items = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(f"GROUP#{group_name}")
            & Key(key_structure.sort_key).begins_with("SERVICESLINES")
        ),
        facets=(TABLE.facets["root_services_toe_lines"],),
        index=None,
        table=TABLE,
    )
    group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        group_name
    )
    nicknames = {
        root.id: root.state.nickname
        for root in group_roots
        if isinstance(root, GitRootItem)
    }
    new_sks = tuple(
        format_sk(
            nicknames,
            item[TABLE.primary_key.sort_key],
        )
        for item in items
    )
    items_to_update = [
        (item, new_sk)
        for item, new_sk in zip(items, new_sks)
        if item[TABLE.primary_key.sort_key] != new_sk
    ]
    keys = {
        (item[TABLE.primary_key.partition_key], new_sk)
        for item, new_sk in zip(items, new_sks)
    }
    items_to_write = []
    for item, new_sk in items_to_update:
        if (item[TABLE.primary_key.partition_key], new_sk) in keys:
            items_to_write.append((item, new_sk))
            keys.discard((item[TABLE.primary_key.partition_key], new_sk))
    await collect(
        tuple(
            operations.batch_write_item(
                items=tuple(
                    {
                        **item,
                        TABLE.primary_key.sort_key: new_sk,
                    }
                    for item, new_sk in items_to_write_chunk
                ),
                table=TABLE,
            )
            for items_to_write_chunk in chunked(items_to_write, 25)
        ),
        workers=100,
    )
    await collect(
        tuple(
            operations.batch_delete_item(
                keys=tuple(
                    PrimaryKey(
                        partition_key=item[TABLE.primary_key.partition_key],
                        sort_key=item[TABLE.primary_key.sort_key],
                    )
                    for item, _ in items_chunk
                ),
                table=TABLE,
            )
            for items_chunk in chunked(items_to_update, 20)
        ),
        workers=100,
    )


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    group_names_len = len(group_names)

    await collect(
        tuple(
            remove_nicknames(loaders, group_name, count / group_names_len)
            for count, group_name in enumerate(group_names)
        ),
        workers=3,
    )
    print("Success: True")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
