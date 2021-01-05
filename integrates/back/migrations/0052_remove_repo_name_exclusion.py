# /usr/bin/env python3
"""
This migration removes the repository name from the exclusion patterns
used to define which file should not be reviewed by analysts

Execution Time: 2021-01-05 18:23 UTC-5
Finalization Time: 2021-01-05 18:27 UTC-5
"""
# Standard
import os
import urllib
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
from backend.domain.project import get_active_projects


def get_repo_from_url(url: str) -> str:
    url_obj = urllib.parse.urlparse(url)
    url_path = urllib.parse.unquote_plus(url_obj.path)
    repo = os.path.basename(url_path)

    if repo.endswith('.git'):
        repo = repo[0:-4]
    return repo


async def update_root(group_name: str, root: Dict[str, Any]) -> None:
    last_state = root['historic_state'][-1]
    repo_name = get_repo_from_url(root['url'])
    filter_config: Dict[str, List[str]] = {
        **last_state['filter'],
        'exclude': [
            pattern.replace(f'{repo_name}/', '')
            for pattern in last_state['filter']['exclude']
        ],
    }

    new_state: Dict[str, Any] = {
        **last_state,
        'filter': filter_config,
    }

    await root_dal.update(
        group_name, root['sk'],
        {'historic_state': [*root['historic_state'], new_state]}
    )


async def main() -> None:
    groups: List[str] = await get_active_projects()
    print(f'[INFO] Found {len(groups)} groups')

    for group_name in groups:
        roots = await root_dal.get_roots_by_group(group_name)
        print(f'[INFO] Working on {group_name} with {len(roots)} roots')
        await collect(update_root(group_name, root) for root in roots)


if __name__ == '__main__':
    run(main())
