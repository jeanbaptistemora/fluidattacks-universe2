# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
"""
This migration adds missing nicknames to roots affected by a bug

Execution Time:    2021-07-23 at 17:47:36 UTC-05
Finalization Time: 2021-07-23 at 17:47:42 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from dynamodb.types import (
    GitRootState,
    RootItem,
)
from groups.dal import (  # pylint: disable=import-error
    get_active_groups,
)
from roots import (
    dal as roots_dal,
    domain as roots_domain,
)
import time


async def update_root(root: RootItem) -> None:
    print("Working on", root.id, root.metadata.url)
    await roots_dal.update_root_state(
        group_name=root.group_name,
        root_id=root.id,
        state=GitRootState(
            environment_urls=root.state.environment_urls,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=root.state.modified_by,
            modified_date=root.state.modified_date,
            # pylint: disable=protected-access
            nickname=roots_domain._format_root_nickname("", root.metadata.url),
            other=root.state.other,
            reason=root.state.reason,
            status=root.state.status,
        ),
    )


async def update_group(group_name: str) -> None:
    roots = await roots_domain.get_roots(group_name=group_name)
    affected_roots = tuple(root for root in roots if root.state.nickname == "")

    if affected_roots:
        print(f"Fixing {len(affected_roots)} roots for group {group_name}")
        await collect(tuple(update_root(root) for root in affected_roots))


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
