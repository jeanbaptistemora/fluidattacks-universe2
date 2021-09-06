# pylint: disable=invalid-name
"""
This migration moves the branch and url attributes from the metadata to
the state items on git roots

Execution Time:
Finalization Time:
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
    GitRootItem,
    GitRootState,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from groups.dal import (
    get_active_groups,
)
import simplejson as json  # type: ignore
import time
from typing import (
    List,
)


async def update_root(root: GitRootItem) -> None:
    historic_state: List[GitRootState] = await RootStatesLoader().load(root.id)
    # Update historic states
    await collect(
        tuple(
            operations.update_item(
                item={
                    **json.loads(json.dumps(state)),
                    "branch": root.state.branch,
                    "url": root.state.url,
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
        group_name=root.group_name, root_id=root.id, state=root.state
    )
    # Update metadata
    await operations.update_item(
        item={"branch": None, "url": None},
        key=PrimaryKey(
            partition_key=f"ROOT#{root.id}",
            sort_key=f"GROUP#{root.group_name}",
        ),
        table=TABLE,
    )


async def main() -> None:
    groups = await get_active_groups()
    group_roots = await GroupRootsLoader().load_many(groups)
    await collect(
        tuple(
            update_root(root)
            for roots in group_roots
            for root in roots
            if isinstance(root, GitRootItem)
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
