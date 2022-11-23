# type: ignore

# /usr/bin/env python3
# pylint: disable=invalid-name
"""
This migration corrects exclude patterns that aim to define a complete
directory.

node_modules/*  ->  node_modules/

Execution Time:    2021-01-06 10:14 UTC-5
Finalization Time: 2021-01-06 10:18 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from groups.domain import (
    get_active_groups,
)
from roots import (
    dal as roots_dal,
)
from typing import (
    Any,
    Dict,
    List,
)


async def update_root(group_name: str, root: Dict[str, Any]) -> None:
    last_state = root["historic_state"][-1]
    filter_config: Dict[str, List[str]] = {
        **last_state["filter"],
        "exclude": [
            pattern[:-1] if pattern.endswith("/*") else pattern
            for pattern in last_state["filter"]["exclude"]
        ],
    }

    new_state: Dict[str, Any] = {
        **last_state,
        "filter": filter_config,
    }

    await roots_dal.update_legacy(
        group_name,
        root["sk"],
        {"historic_state": [*root["historic_state"], new_state]},
    )


async def main() -> None:
    groups: List[str] = await get_active_groups()
    print(f"[INFO] Found {len(groups)} groups")

    for group_name in groups:
        roots = await roots_dal.get_roots_by_group_legacy(group_name)
        print(f"[INFO] Working on {group_name} with {len(roots)} roots")
        await collect(update_root(group_name, root) for root in roots)


if __name__ == "__main__":
    run(main())
