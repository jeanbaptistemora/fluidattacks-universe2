# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration add a default cloning status for roots

Execution Time:
Finalization Time:
"""
# Standard
import os
from typing import (
    Any,
    Dict,
    List,
)

# Third party
from aioextensions import (
    collect,
    run,
)

# Local
from backend.dal import root as root_dal
from backend.utils import datetime

STAGE: str = os.environ['STAGE']
SERVICES_REPO_DIR: str = f'{os.getcwd()}/services'


async def update_root(group_name: str, root_id: str) -> None:
    status: Dict[str, Any] = {
        'status': 'UNKNOWN',
        'date': datetime.get_as_str(datetime.get_now()),
        'message': 'root created',
    }
    await root_dal.update(
        group_name,
        root_id,
        {'historic_cloning_status': [status]},
    )


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, 'groups'))
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        print(f'[INFO] Working on {group_name}')
        roots = await root_dal.get_roots_by_group(group_name)
        await collect(update_root(group_name, root) for root in roots)


if __name__ == '__main__':
    run(main())
