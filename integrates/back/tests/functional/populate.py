# Standard libraries
from typing import (
    Awaitable,
    Any,
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
from backend.dal.helpers.dynamodb import (
    async_delete_item,
    async_scan,
)
from backend.typing import (
    DynamoDelete ,
)


DYNAMO_TABLES: Dict[str, Dict[str, str]] = {
    'FI_comments': {
        'pk': 'finding_id',
        'sk': 'user_id',
    },
    'FI_findings': {
        'pk': 'finding_id',
    },
    'FI_forces': {
        'pk': 'subscription',
        'sk': 'execution_id',
    },
    'FI_project_access': {
        'pk': 'user_email',
        'sk': 'project_name',
    },
    'FI_projects': {
        'pk': 'project_name',
    },
    'FI_toe': {
        'pk': 'project',
    },
    'FI_users': {
        'pk': 'email',
    },
    'FI_vulnerabilities': {
        'pk': 'finding_id',
        'sk': 'UUID',
    },
    'fi_authz': {
        'pk': 'subject',
        'sk': 'object',
    },
    'fi_events': {
        'pk': 'event_id',
    },
    'fi_organizations': {
        'pk': 'pk',
        'sk': 'sk',
    },
    'fi_portfolios': {
        'pk': 'organization',
        'sk': 'tag'
    },
    'fi_project_comments': {
        'pk': 'project_name',
        'sk': 'user_id',
    },
    'fi_roots': {
        'pk': 'pk',
        'sk': 'sk',
    },
    'fi_subscriptions': {
        'pk': 'pk',
        'sk': 'sk',
    },
    'integrates': {
        'pk': 'pk',
        'sk': 'sk',
    },
}


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
    coroutines_org_users.extend([
        dal_organization.add_user(
            (await dal_organization.get_by_name(
                org['name'],
                ['id'],
            ))['id'],
            user,
        )
        for org in data
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


async def populate_db(data: Dict[str, Any]) -> bool:
    success: bool = False
    keys: List[str, str] = data.keys()

    if 'users' in keys:
        success = await populate_users(data['users'])

    if 'orgs' in keys:
        success = success and await populate_orgs(data['orgs'])

    if 'policies' in keys:
        success = success and await populate_policies(data['policies'])

    return success


async def clean_table(table: str, key_attrs: Dict[str, str]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    scan_attrs: Dict[str, Any] = {
        'ExpressionAttributeNames': {'#pk': key_attrs['pk']},
        'ProjectionExpression': '#pk',
    }
    if 'sk' in key_attrs.keys():
        scan_attrs['ExpressionAttributeNames']['#sk'] = key_attrs['sk']
        scan_attrs['ProjectionExpression'] = '#pk, #sk'
    items: List[Any] = await async_scan(
        table,
        scan_attrs,
    )
    for item in items:
        key: Dict[str, str] = {key_attrs['pk']: item[key_attrs['pk']]}
        if 'sk' in key_attrs.keys():
            key[key_attrs['sk']] = item[key_attrs['sk']]
        coroutines.append(
            async_delete_item(
                table,
                DynamoDelete(
                    Key=key,
                ),
            )
        )
    return all(await collect(coroutines))


async def clean_db() -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    coroutines.extend([
        clean_table(name, attrs)
        for name, attrs in DYNAMO_TABLES.items()
    ])
    return all(await collect(coroutines))
