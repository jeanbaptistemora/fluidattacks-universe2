"""
This migration will clean IMAMURA from users
that already have another org.

Execution Time:    2020-12-01 at 14:41:39 UTC-05
Finalization Time: 2020-12-01 at 14:46:30 UTC-05
"""
import time
import os
import csv

from typing import List, cast
from asyncio import run

from aioextensions import (
    collect,
)

from backend.dal import (
    organization as org_dal
)
from backend.domain import (
    organization as org_domain
)
from backend.exceptions import UserNotInOrganization

STAGE: str = os.environ['STAGE']


async def remove_user_from_imamura(user: str, org_id: str) -> bool:
    try:
        success: bool = cast(bool, await org_domain.remove_user(org_id, user))
        if success:
            print(f'[INFO] User {user} removed from imamura')
        else:
            print(f'[ERROR] Failed to remove user {user} from imamura')
        return success
    except UserNotInOrganization:
        print(f'[INFO] User {user} already remove from imamura')
        return True


async def main() -> None:
    print(f'[INFO] Starting migration 0036')
    user_emails: List[str] = []
    org = await org_dal.get_by_name('imamura', ['id'])
    with open('app/migrations/users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'imamura' in row['Organizations']:
                user_emails.append(row['email'])
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
