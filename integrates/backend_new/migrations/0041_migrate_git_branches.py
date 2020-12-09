# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration splits the url paths from the branch in git roots

Execution Time:
Finalization Time:
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


async def split_paths_from_branch(
    group_name: str,
    root: Dict[str, Any]
) -> None:
    branch: str = root['branch'].split('/')[-1]
    paths: str = '/'.join(root['branch'].split('/')[:-1])
    trailing: str = '' if root['url'].endswith('/') else '/'
    url: str = f'{root["url"]}{trailing}{paths}'

    if STAGE == 'test':
        print('[INFO] Will migrate', root['sk'], branch, url)
    else:
        await root_dal.update(
            group_name,
            root['sk'],
            {'branch': branch, 'url': url}
        )


async def main() -> None:
    groups: List[str] = os.listdir(os.path.join(SERVICES_REPO_DIR, 'groups'))
    print(f'[INFO] Found {len(groups)} groups')
    for group_name in groups:
        print(f'[INFO] Working on {group_name}')
        roots = await root_dal.get_roots_by_group(group_name)

        await collect(
            split_paths_from_branch(group_name, root)
            for root in roots
        )


if __name__ == '__main__':
    run(main())
