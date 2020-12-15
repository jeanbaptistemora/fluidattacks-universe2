# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration removes old paths and policy attributes from filter configs

Execution Time:
 2020-12-14 20:51:42 UTC-5
"""
# Standard
import os
from typing import Any, Dict, List

# Third party
from aioextensions import collect, run

# Local
from backend.dal import root as root_dal


STAGE: str = os.environ['STAGE']
SERVICES_REPO_DIR: str = f'{os.getcwd()}/services'


async def update_filter(
    group_name: str,
    root: Dict[str, Any]
) -> None:
    states_to_update = [
        {
            **state,
            'filter': {
                'exclude': state['filter']['exclude'],
                'include': state['filter']['include']
            }
        }
        for state in root['historic_state']
    ]

    if STAGE == 'test':
        print('[INFO] Will migrate', len(states_to_update), 'for', root['sk'])
        print(states_to_update)
    else:
        await root_dal.update(
            group_name,
            root['sk'],
            {'historic_state': states_to_update}
        )


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, 'groups'))
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        print(f'[INFO] Working on {group_name}')
        roots = await root_dal.get_roots_by_group(group_name)

        await collect(
            update_filter(group_name, root)
            for root in roots
        )


if __name__ == '__main__':
    run(main())
