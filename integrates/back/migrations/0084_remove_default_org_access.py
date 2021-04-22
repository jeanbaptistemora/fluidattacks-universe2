"""
This migration aims to remove default organization access
to user with access to a group in any other organization

Execution Time:    2021-04-21 at 20:30:16 UTC-05
Finalization Time: 2021-04-21 at 20:33:58 UTC-05
"""
# Standard libraries
from itertools import chain
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import Attr

# Local libraries
from backend import authz
from groups import domain as groups_domain
from organizations import domain as orgs_domain
from users import dal as users_dal
from __init__ import FI_DEFAULT_ORG


USERS_TABLE_NAME = 'FI_users'


async def remove_default_org_access(
    email: str,
    default_org_id: str,
) -> bool:
    enforcer = await authz.get_user_level_enforcer(email)
    if enforcer('self', 'keep_default_organization_access'):
        return True
    orgs_ids: List[str] = await orgs_domain.get_user_organizations(email)
    if len(orgs_ids) > 1 and default_org_id in orgs_ids:
        groups: List[str] = list(chain.from_iterable(
            await collect([
                groups_domain.get_groups_by_user(
                    user_email=email,
                    organization_id=org_id
                )
                for org_id in orgs_ids if org_id != default_org_id
            ])
        ))
        if groups:
            print(f'User {email} has access to more orgs than the default')
            return await orgs_domain.remove_user(default_org_id, email)
    
    return True


async def main() -> None:
    users = await users_dal.get_all(Attr('registered').eq(True), 'email')
    default_org = await orgs_domain.get_by_name(FI_DEFAULT_ORG.lower())

    success = all(await collect(
        [
            remove_default_org_access(
                str(user['email']),
                str(default_org['id'])
            )
            for user in users
        ],
        workers=16
    ))

    print(f'Success: {success}')


if __name__ == '__main__':
    run(main())
