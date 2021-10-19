# pylint: disable=invalid-name
"""
It aims to have two toe lines facets for the same group. The lines keyword in
the toe lines facet is going to be reserved for the last facet version of toe
lines.

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
    keys,
    operations,
)
from groups import (
    domain as groups_domain,
)
import time


async def copy_lines(group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_lines"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    line_key = primary_key.sort_key.split("#")[0]
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(line_key)
        ),
        facets=(TABLE.facets["root_toe_lines"],),
        index=None,
        table=TABLE,
    )
    await operations.batch_write_item(
        items=tuple(
            {
                **item,
                TABLE.primary_key.sort_key: (
                    item[TABLE.primary_key.sort_key].replace(
                        "LINES", "SERVICESLINES"
                    )
                ),
            }
            for item in results
        ),
        table=TABLE,
    )


async def main() -> None:
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    await collect(tuple(map(copy_lines, group_names)), workers=50)
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
