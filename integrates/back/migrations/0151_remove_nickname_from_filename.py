# pylint: disable=invalid-name
"""
Remove the root nickname from the toe lines filename.

"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups import (
    domain as groups_domain,
)
import time


def format_sk(sk: str) -> str:
    sk.split("#", 4)
    sort_key_items = sk.split("#", 4)
    filename = sort_key_items.pop()
    _, new_filename = filename.split("/", 1)
    return "#".join([*sort_key_items, new_filename])


async def remove_nicknames(group_name: str, progress: float) -> None:
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
    await operations.batch_write_item(
        items=tuple(
            {
                **item,
                TABLE.primary_key.sort_key: (
                    format_sk(item[TABLE.primary_key.sort_key])
                ),
            }
            for item in items
        ),
        table=TABLE,
    )
    await collect(
        tuple(
            operations.delete_item(
                primary_key=PrimaryKey(
                    partition_key=item[TABLE.primary_key.partition_key],
                    sort_key=item[TABLE.primary_key.sort_key],
                ),
                table=TABLE,
            )
            for item in items
        ),
    )


async def main() -> None:
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    group_names_len = len(group_names)

    await collect(
        tuple(
            remove_nicknames(group_name, count / group_names_len)
            for count, group_name in enumerate(group_names)
        )
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
