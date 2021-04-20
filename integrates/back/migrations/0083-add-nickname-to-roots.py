# /usr/bin/env python3
# -.- coding: utf-8 -.-
"""
This migration add the nickname value to each root
if found any duplicate adds a number to difference
each nickname.

Execution Time:    2021-03-19 at 09:24:06 UTC-05
Finalization Time: 2021-03-19 at 09:35:09 UTC-05
"""
# Standard
import os
import time
from typing import Any, Dict, List, Set

# Third party
from aioextensions import collect, run

# Local
from groups import dal as groups_dal
from roots import dal as roots_dal
from roots import domain as roots_domain


async def update_filter(
    group_name: str,
    root: Dict[str, Any],
    nicknames: Dict[str, int],
) -> None:

    url: str = root['url']

    is_not_unique = True

    nickname: str = roots_domain.format_root_nickname(root.get('nickname', ''), url)
    format_nickname: str = nickname

    while is_not_unique:
        if format_nickname in nicknames.keys():
            counter = nicknames[nickname]
            format_nickname = f'{nickname}_{counter}'
        else:
            is_not_unique = False

    print(
        f'[INFO] repository with name: "{nickname}" '
        f'will have a nickname: "{format_nickname}" '
    )

    await roots_dal.update_legacy(
        group_name,
        root['sk'],
        {'nickname': format_nickname}
    )

    return nickname


async def work_with_group(group_name: str):
    print(f'[INFO] Working on {group_name}')
    roots = await roots_dal.get_roots_by_group_legacy(group_name)
    nicknames: Dict[str, int] = {}
    for root in roots:
        nickname = await update_filter(group_name, root, nicknames)
        if nicknames.get(nickname, ''):
            nicknames[nickname] += 1
        else:
            nicknames[nickname] = 2

async def main() -> None:
    groups = await groups_dal.get_all(data_attr='project_name')
    await collect(
        work_with_group(group_name['project_name'])
        for group_name in groups
    )


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
