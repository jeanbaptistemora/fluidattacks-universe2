# Standard libraries
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
from backend.dal import (
    organization as dal_organization,
    user as dal_user,
)


async def populate_users(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_user.create(
            user['email'],
            user,
        )
        for user in data
    ])
    return all(await collect(coroutines))


async def populate_orgs(data: List[Any]) -> bool:
    success: bool = False
    coroutines_orgs: List[Awaitable[bool]] = []
    coroutines_org_users: List[Awaitable[bool]] = []
    coroutines_orgs.extend([
        dal_organization.create(
            org['name'],
        )
        for org in data
    ])
    success = all(await collect(coroutines_orgs))
    for org in data:
        org_id: str = (await dal_organization.get_by_name(
            org['name'],
            ['id'],
        ))['id']
        coroutines_org_users.extend([
            dal_organization.add_user(
                org_id,
                user,
            )
            for user in org['users']
        ])
    success = success and all(await collect(coroutines_org_users))
    return success


async def populate_policies(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_user.put_subject_policy(
            dal_user.SubjectPolicy(
                level=policy['level'],
                subject=policy['subject'],
                object=(
                    await dal_organization.get_by_name(
                        policy['object'],
                        ['id'],
                    ))['id'] \
                    if policy['level'] == 'organization' \
                    else policy['object'],
                role=policy['role'],
            ),
        )
        for policy in data
    ])
    return all(await collect(coroutines))


async def populate(data: Dict[str, Any]) -> bool:
    success: bool = False
    keys: List[str, str] = data.keys()

    if 'users' in keys:
        success = await populate_users(data['users'])

    if 'orgs' in keys:
        success = success and await populate_orgs(data['orgs'])

    if 'policies' in keys:
        success = success and await populate_policies(data['policies'])

    return success
