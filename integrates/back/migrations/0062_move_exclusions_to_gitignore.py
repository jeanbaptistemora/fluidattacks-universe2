"""
This migration aims to migrate the old filter field to the newer
and simpler gitignore

Execution Time:
Finalization Time:
"""
# Standard library
import os
import time
from typing import Any, Dict, List

# Third party libraries
from aioextensions import collect, run

# Local libraries
from backend.dal import project as group_dal, root as root_dal


STAGE = os.environ['STAGE']


def exclude_filter(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: value
        for (key, value) in state.items()
        if key != 'filter'
    }


async def migrate(group_name: str) -> None:
    group_roots = await root_dal.get_roots_by_group(group_name)

    if group_roots:
        if STAGE == 'test':
            print(
                '[INFO] Will migrate',
                len(group_roots),
                'roots for',
                group_name
            )
        else:
            await collect(
                root_dal.update(
                    root['pk'],
                    root['sk'],
                    {
                        'historic_state': [
                            {
                                **exclude_filter(state),
                                'environment_urls': state.get(
                                    'environment_urls',
                                    []
                                ),
                                'gitignore': state['filter']['exclude'],
                            }
                            for state in root['historic_state']
                        ]
                    }
                )
                for root in group_roots
            )


async def main() -> None:
    print('[INFO] Starting migration 0062')
    groups = await group_dal.get_all(data_attr='project_name')
    await collect(
        migrate(group['project_name'])
        for group in groups
    )
    print('[INFO] Migration 0062 finished')


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
