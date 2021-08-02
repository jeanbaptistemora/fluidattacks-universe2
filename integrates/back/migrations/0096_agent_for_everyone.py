# pylint: disable=invalid-name
"""
This migration enables the devsecops agent to all active groups

Execution Time:    2021-07-02 at 18:27:51 UTC-05
Finalization Time: 2021-07-02 at 18:29:21 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from forces.domain import (
    add_forces_user,
)
from graphql.type import (
    GraphQLResolveInfo,
)
from groups.dal import (
    get_active_groups,
    get_attributes,
    update,
)
import time


async def update_group(group_name: str) -> None:
    historic_config = (
        await get_attributes(group_name, ["historic_configuration"])
    )["historic_configuration"]

    await update(
        group_name,
        {
            "historic_configuration": [
                *historic_config[:-1],
                {
                    **historic_config[-1],
                    "has_forces": True,
                },
            ]
        },
    )

    info = GraphQLResolveInfo(
        None, None, None, None, None, None, None, None, None, None, {}
    )
    await add_forces_user(info, group_name)


async def main() -> None:
    groups = await get_active_groups()
    await collect(tuple(update_group(group_name) for group_name in groups))


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
