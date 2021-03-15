# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration converts the GitRoots filters into glob expressions
new expressions must be analyzed relative to the repository, not to the fusion

Execution Time:
Finalization Time:
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
from backend.domain.project import get_active_projects
from newutils import datetime
from roots import dal as roots_dal


def regex_to_glob(regex: str) -> str:
    glob = regex[1:-1].replace('.*', '*')
    if glob.startswith('*/'):
        return glob[2:]
    return glob


async def update_root(group_name: str, root: Dict[str, Any]) -> None:
    last_state = root['historic_state'][-1]
    filter_config: Dict[str, List[str]] = {
        'exclude': list(map(regex_to_glob, last_state['filter']['exclude'])),
        'include': list(map(regex_to_glob, last_state['filter']['include'])),
    }

    new_state: Dict[str, Any] = {
        **last_state,
        'date': datetime.get_as_str(datetime.get_now()),
        'filter': filter_config,
    }

    await roots_dal.update_legacy(
        group_name, root['sk'],
        {'historic_state': [*root['historic_state'], new_state]})


async def main() -> None:
    groups: List[str] = await get_active_projects()
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        roots = await roots_dal.get_roots_by_group_legacy(group_name)
        print(f'[INFO] Working on {group_name} with {len(roots)} roots')
        await collect(update_root(group_name, root) for root in roots)


if __name__ == '__main__':
    run(main())
