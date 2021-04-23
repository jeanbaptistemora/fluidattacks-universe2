#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration sets all toe's new sorts_risk_level attribute
to zero

"""

# Standard libraries
from itertools import chain

# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from groups.dal import get_active_groups
from toe.lines.domain import (
    get_by_group,
    update as update_toe,
)


async def update_sorts_risk_level(toe: GitRootToeLines) -> bool:
    toe = toe._replace(sorts_risk_level=0)
    await update_toe(toe)


async def main() -> None:
    groups = await get_active_groups()
    groups_toes: List[GitRootToeLines] = list(chain.from_iterable(
        await collect([
            get_by_group(group)
            for group in groups
        ])
    ))

    await collect(
        [
            update_sorts_risk_level(group_toe)
            for group_toe in groups_toes
        ],
        workers=16
    )


if __name__ == '__main__':
    run(main())
