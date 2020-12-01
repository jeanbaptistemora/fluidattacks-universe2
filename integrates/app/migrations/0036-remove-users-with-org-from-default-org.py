"""
This migration will clean IMAMURA from users
that already have another org.

Execution Time:
Finalization Time:
"""
import time
import os

from typing import List, cast
from asyncio import run

from aioextensions import (
    collect,
)

from backend.domain import (
    organization as org_domain
)
from backend.dal import (
    organization as org_dal
)

STAGE: str = os.environ['STAGE']


async def remove_user_from_imamura(user: str, org_id: str) -> bool:
    print(f'[INFO] Removing {user} from imamura')
    return cast(bool, await org_domain.remove_user(org_id, user))


async def main() -> None:
    print(f'[INFO] Starting migration 0036')
    user_emails: List[str] = []
    user_list = open("app/migrations/users.csv", "r")
    users = user_list.read().split("\n")
    users = list(filter(lambda x: 'imamura' in x, users))
    user_list.close()
    user_emails = list(map(lambda x: x.split(",")[0], users))
    user_emails.sort()
    org = await org_dal.get_by_name('imamura', ['id'])
    if STAGE == 'test':
        for user in user_emails:
            print(f'[INFO] User {user} will be removed from org with id {org["id"]}')
    else:
        users_removed = await collect(
            remove_user_from_imamura(user, str(org['id']))
            for user in user_emails
        )
        if False in list(users_removed):
            print(f'[INFO] Migration fails')
    print(f'[INFO] End migration 0036\n')


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
