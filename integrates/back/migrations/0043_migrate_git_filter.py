# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration copies filter configs to a new format in git roots

Execution Time: 2020-12-14 20:48:48 UTC-5
Finalization Time: 2020-12-14 20:51:42 UTC-5
"""
# Standard
import os
from typing import Any, Dict, List

# Third party
from aioextensions import collect, run

# Local
from roots import dal as roots_dal


STAGE: str = os.environ['STAGE']
SERVICES_REPO_DIR: str = f'{os.getcwd()}/services'


def format_new_filter(filter_config: Dict[str, Any]) -> Dict[str, List[str]]:
    if filter_config:
        if filter_config['policy'] == 'EXCLUDE':
            return {
                **filter_config,
                'exclude': filter_config['paths'],
                'include': ['^.*$']
            }

        # INCLUDE
        return {
            **filter_config,
            'exclude': [],
            'include': filter_config['paths']
        }

    # NONE
    return {'exclude': [], 'include': ['^.*$']}


async def update_filter(
    group_name: str,
    root: Dict[str, Any]
) -> None:
    states_to_update = [
        {
            **state,
            'filter': format_new_filter(state.get('filter'))
        }
        for state in root['historic_state']
    ]

    if STAGE == 'test':
        print('[INFO] Will migrate', len(states_to_update), 'for', root['sk'])
        print(states_to_update)
    else:
        await roots_dal.update_legacy(
            group_name,
            root['sk'],
            {'historic_state': states_to_update}
        )


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, 'groups'))
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        print(f'[INFO] Working on {group_name}')
        roots = await roots_dal.get_roots_by_group_legacy(group_name)

        await collect(
            update_filter(group_name, root)
            for root in roots
        )


if __name__ == '__main__':
    run(main())
