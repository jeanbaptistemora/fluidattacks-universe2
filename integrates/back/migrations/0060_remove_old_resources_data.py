"""
This migration aims to remove old repos and envs data
now that they've been replaced by git roots (new scope module)

Execution Time: 2021-01-19 at 15:32:05 UTC-05
Finalization Time: 2021-01-19 at 15:32:29 UTC-05
"""
# Standard library
import os
import time

# Third party libraries
from aioextensions import collect, run

# Local libraries
from groups import dal as groups_dal


STAGE = os.environ['STAGE']


async def remove_old_data(group_name: str) -> None:
    if STAGE == 'test':
        print('[INFO] Will clean', group_name)
    else:
        await groups_dal.update(
            group_name,
            {'environments': None, 'repositories': None}
        )


async def main() -> None:
    print('[INFO] Starting migration 0060')
    groups = await groups_dal.get_all(data_attr='project_name')
    await collect(
        remove_old_data(group['project_name'])
        for group in groups
    )
    print('[INFO] Migration 0060 finished')


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
