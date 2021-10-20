# pylint: disable=invalid-name
"""
This migration moves the host, path, port and protocol attributes from the
metadata to the state items on url roots

Execution Time:    2021-09-10 at 16:35:36 UTC
Finalization Time: 2021-09-10 at 16:37:02 UTC
"""

from aioextensions import (
    collect,
    run,
)
from db_model import (
    roots as roots_model,
    TABLE,
)
from db_model.roots.get import (
    GroupRootsLoader,
    RootStatesLoader,
)
from db_model.roots.types import (
    URLRootItem,
    URLRootState,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups.dal import (
    get_all,
)
import time
from typing import (
    List,
)


async def update_root(root: URLRootItem) -> None:
    historic_state: List[URLRootState] = await RootStatesLoader().load(root.id)
    # Update historic states
    await collect(
        tuple(
            operations.update_item(
                item={
                    "host": root.state.host,
                    "path": root.state.path,
                    "port": root.state.port,
                    "protocol": root.state.protocol,
                },
                key=PrimaryKey(
                    partition_key=f"ROOT#{root.id}",
                    sort_key=f"STATE#{state.modified_date}",
                ),
                table=TABLE,
            )
            for state in historic_state
        )
    )
    # Update latest state
    await roots_model.update_root_state(
        current_value=root.state,
        group_name=root.group_name,
        root_id=root.id,
        state=root.state,
    )
    # Update metadata
    await operations.update_item(
        item={"host": None, "path": None, "port": None, "protocol": None},
        key=PrimaryKey(
            partition_key=f"ROOT#{root.id}",
            sort_key=f"GROUP#{root.group_name}",
        ),
        table=TABLE,
    )


async def main() -> None:
    groups = tuple(
        group["project_name"]
        for group in await get_all(data_attr="project_name")
    )
    group_roots = await GroupRootsLoader().load_many(groups)
    await collect(
        tuple(
            update_root(root)
            for roots in group_roots
            for root in roots
            if isinstance(root, URLRootItem)
        )
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
