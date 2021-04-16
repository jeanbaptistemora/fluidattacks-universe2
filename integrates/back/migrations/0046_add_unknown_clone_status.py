# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration add a default cloning status for roots

Execution Time: Thu Dec 17 08:09:46 -05 2020
Finalization Time: Thu Dec 17 08:14:32 -05 2020
"""
# Standard
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
from groups.domain import get_active_groups
from newutils import datetime
from roots import dal as roots_dal


async def update_root(group_name: str, root_id: Dict[str, Any]) -> None:
    status: Dict[str, Any] = {
        'status': 'UNKNOWN',
        'date': datetime.get_as_str(datetime.get_now()),
        'message': 'root created',
    }
    await roots_dal.update_legacy(
        group_name,
        root_id['sk'],
        {'historic_cloning_status': [status]},
    )


async def main() -> None:
    groups: List[str] = await get_active_groups()
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        roots = await roots_dal.get_roots_by_group_legacy(group_name)
        print(f'[INFO] Working on {group_name} with {len(roots)} roots')
        await collect(update_root(group_name, root) for root in roots)


if __name__ == '__main__':
    run(main())
