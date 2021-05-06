# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration adds an attribute for the new service in a group's
historic configuration

Execution Time:
Finalization Time:
"""
# Standard
import time

# Third party
from aioextensions import collect, run

# Local
from groups.dal import get_active_groups, get_attributes, update


async def update_group(group_name: str) -> bool:
    historic_config = (await get_attributes(
        group_name,
        ['historic_configuration']
    ))['historic_configuration']

    await update(group_name, {
        'historic_configuration': [
            *historic_config[:-1],
            {
                **historic_config[-1],
                'has_skims': historic_config[-1]['has_drills']
            }
        ]
    })


async def main() -> None:
    groups = await get_active_groups()
    await collect(tuple(
        update_group(group_name)
        for group_name in groups
    ))


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
