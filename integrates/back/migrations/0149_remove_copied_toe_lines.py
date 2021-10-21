# pylint: disable=invalid-name
"""
Remove the toe lines that were copied with 0147_copy_toe_lines.

Execution Time:
Finalization Time:
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


async def remove_lines(group_name: str) -> None:
    key_structure = TABLE.primary_key
    items = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(f"GROUP#{group_name}")
            & Key(key_structure.sort_key).begins_with("LINES")
        ),
        facets=(TABLE.facets["root_services_toe_lines"],),
        index=None,
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
        )
    )


async def main() -> None:
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    await collect(tuple(map(remove_lines, group_names)), workers=50)
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
