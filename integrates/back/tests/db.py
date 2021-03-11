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
from events import (
    dal as dal_event,
)
from backend.dal import (
    finding as dal_finding,
    project as dal_group,
    available_name as dal_name,
    organization as dal_organization,
    root as dal_root,
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
            f'ORG#{org["id"]}',
            org['name'],
            org['policy'],
        )
        for org in data if org['policy']
    ])
    success = success and all(await collect(coroutines))
    return success



async def populate_groups(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    data_dump: str = json.dumps(data)
    data_parsed: List[Any] = json.loads(data_dump, parse_float=Decimal)
    coroutines.extend([
        dal_group.create(
            group,
        )
        for group in data_parsed
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


async def populate_roots(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_root.create(
            root['pk'],
            root,
        )
        for root in data
    ])
    return all(await collect(coroutines))


async def populate_consultings(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_group.add_comment(
            consulting['project_name'],
            consulting['email'],
            consulting,
        )
        for consulting in data
    ])
    return all(await collect(coroutines))


async def populate_events(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_event.create(
            event['event_id'],
            event['project_name'],
            event,
        )
        for event in data
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
    coroutines.extend([
        dal_group.update_access(
            policy['subject'],
            policy['object'],
            {'has_access': True},
        )
        for policy in data if policy['level'] == 'group'
    ])
    return all(await collect(coroutines))


async def populate(data: Dict[str, Any]) -> bool:
    keys: List[str, str] = data.keys()
    coroutines: List[Awaitable[bool]] = []

    if 'users' in keys:
        coroutines.append(populate_users(data['users']))

    if 'names' in keys:
        coroutines.append(populate_names(data['names']))

    if 'orgs' in keys:
        coroutines.append(populate_orgs(data['orgs']))

    if 'groups' in keys:
        coroutines.append(populate_groups(data['groups']))

    if 'findings' in keys:
        coroutines.append(populate_findings(data['findings']))

    if 'consultings' in keys:
        coroutines.append(populate_consultings(data['consultings']))

    if 'vulnerabilities' in keys:
        coroutines.append(populate_vulnerabilities(data['vulnerabilities']))

    if 'roots' in keys:
        coroutines.append(populate_roots(data['roots']))

    if 'events' in keys:
        coroutines.append(populate_events(data['events']))

    if 'policies' in keys:
        coroutines.append(populate_policies(data['policies']))

    return all(await collect(coroutines))
