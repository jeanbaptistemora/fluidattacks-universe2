#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration sets all toe's new sorts_risk_level attribute
to zero

Execution Time:    2021-04-26 at 15:10:02 UTC-05
Finalization Time: 2021-04-26 at 19:35:28 UTC-05
"""


from aioextensions import (
    collect,
    run,
)
from data_containers.toe_lines import (
    GitRootToeLines,
)
from groups.dal import (
    get_active_groups,
)
from itertools import (
    chain,
)
from toe.lines.domain import (
    get_by_group,
    update as update_toe,
)
from typing import (
    List,
)


async def update_sorts_risk_level(toe: GitRootToeLines) -> None:
    toe = toe._replace(sorts_risk_level=0)
    await update_toe(toe)


async def main() -> None:
    groups = await get_active_groups()
    groups_toes: List[GitRootToeLines] = list(
        chain.from_iterable(
            await collect([get_by_group(group) for group in groups])
        )
    )
    print(f"We have {len(groups)} groups and {len(groups_toes)} toes in total")

    await collect(
        [update_sorts_risk_level(group_toe) for group_toe in groups_toes],
        workers=1024,
    )
    print("Migration finished")


if __name__ == "__main__":
    run(main())
