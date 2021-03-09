# Standard libraries
import json
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
from backend.dal import (
    finding as dal_finding,
    project as dal_group,
    available_name as dal_name,
    organization as dal_organization,
    user as dal_user,
    vulnerability as dal_vulnerability,
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


async def populate_names(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_name.create(
            name['name'],
            name['entity'],
        )
        for name in data
    ])
    return all(await collect(coroutines))


async def populate_orgs(data: List[Any]) -> bool:
    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    for org in data:
        coroutines.append(
            dal_organization.create(
                org['name'],
                org['id'],
            )
        )
        for user in org['users']:
            coroutines.append(
                dal_organization.add_user(
                    f'ORG#{org["id"]}',
                    user,
                )
            )
        for group in org['groups']:
            coroutines.append(
                dal_organization.add_group(
                    f'ORG#{org["id"]}',
                    group,
                )
            )
    success = all(await collect(coroutines))
    coroutines = []
    coroutines.extend([
        dal_organization.update(
            org['id'],
            org['name'],
            org['policy'],
        )
        for org in data if org['policy']
    ])
    success = success and all(await collect(coroutines))
    return success



async def populate_groups(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_group.create(
            group,
        )
        for group in data
    ])
    return all(await collect(coroutines))


async def populate_findings(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    data_dump: str = json.dumps(data)
    data_parsed: List[Any] = json.loads(data_dump, parse_float=Decimal)
    coroutines.extend([
        dal_finding.create(
            finding['finding_id'],
            finding['project_name'],
            finding,
        )
        for finding in data_parsed
    ])
    return all(await collect(coroutines))


async def populate_vulnerabilities(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_vulnerability.create(
            vulnerability,
        )
        for vulnerability in data
    ])
    return all(await collect(coroutines))


async def populate_policies(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_user.put_subject_policy(
            dal_user.SubjectPolicy(
                level=policy['level'],
                subject=policy['subject'],
                object=policy['object'],
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

    if 'names' in keys:
        success = success and \
            await populate_names(data['names'])

    if 'orgs' in keys:
        success = success and \
            await populate_orgs(data['orgs'])

    if 'groups' in keys:
        success = success and \
            await populate_groups(data['groups'])

    if 'findings' in keys:
        success = success and \
            await populate_findings(data['findings'])

    if 'vulnerabilities' in keys:
        success = success and \
            await populate_vulnerabilities(data['vulnerabilities'])

    if 'policies' in keys:
        success = success and \
            await populate_policies(data['policies'])

    return success
