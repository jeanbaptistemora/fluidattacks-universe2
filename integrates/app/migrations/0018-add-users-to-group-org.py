#!/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration adds all the users from a group to the organization
the group belongs to

Execution Time: 2020-07-08 15:03:00 UTC-5
Finalization Time: 2020-07-08 15:15:00 UTC-5
"""
import asyncio
import os
from typing import (
    Dict,
    List
)

from aioextensions import (
    collect,
    in_thread,
)
import bugsnag
from backend.dal import organization as org_dal
from backend.domain import (
    organization as org_domain,
    project as group_domain,
    user as user_domain
)
from __init__ import FI_COMMUNITY_PROJECTS, FI_TEST_PROJECTS


STAGE: str = os.environ['STAGE']


async def log(message: str) -> None:
    print(message)
    if STAGE != 'test':
        await in_thread(bugsnag.notify, Exception(message), 'info')


async def main() -> None:
    await log('Starting migration 0018')
    users_already_added: Dict[str, List[str]] = {}
    for group in await in_thread(group_domain.get_alive_projects):
        if group not in FI_COMMUNITY_PROJECTS + FI_TEST_PROJECTS:
            group_org_id = await in_thread(
                group_domain.get_attributes,
                group,
                ['organization']
            )
            group_org_id = group_org_id['organization']
            group_org_name = await org_domain.get_name_by_id(group_org_id)
            group_users = await in_thread(group_domain.get_users, group)
            user_orgs = await collect(
                user_domain.get_attributes(
                    user,
                    ['organization']
                )
                for user in group_users
            )
            user_orgs = [user['organization'] for user in user_orgs]
            await log(
                f'-----\nUsers from group {group} will be updated as follows:'
            )
            if STAGE == 'test':
                await collect(
                    log(
                        f'User {user} will be added to organization '
                        f'{group_org_name}'
                    )
                    for user, user_org in zip(group_users, user_orgs)
                    if user_org != group_org_id and
                        group_org_id not in users_already_added.get(user, [])
                )
            else:
                await collect(
                    org_dal.add_user(group_org_id, user)
                    for user, user_org in zip(group_users, user_orgs)
                    if user_org != group_org_id and
                        group_org_id not in users_already_added.get(user, [])
                )
            for user in group_users:
                if user in users_already_added:
                    if group_org_id not in users_already_added[user]:
                        users_already_added[user].append(group_org_id)
                else:
                    users_already_added[user] = [group_org_id]



if __name__ == '__main__':
    asyncio.run(main())
