# pylint: disable=invalid-name
"""
This migration moves the address and port attributes from the metadata to
the state items on ip roots

Execution Time:    2021-09-09 at 21:44:48 UTC
Finalization Time: 2021-09-09 at 21:45:33 UTC
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
    GitRootState,
    IPRootItem,
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
import simplejson as json  # type: ignore
import time
from typing import (
    List,
)


async def update_root(root: IPRootItem) -> None:
    print(root.id)
    historic_state: List[GitRootState] = await RootStatesLoader().load(root.id)
    # Update historic states
    await collect(
        tuple(
            operations.update_item(
                item={
                    **json.loads(json.dumps(state)),
                    "address": root.state.address,
                    "port": root.state.port,
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
        item={"address": None, "port": None},
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
            if isinstance(root, IPRootItem)
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
