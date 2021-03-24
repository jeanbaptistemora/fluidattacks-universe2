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
    organization as dal_organization,
    user as dal_user,
    vulnerability as dal_vulnerability,
)
from newutils.datetime import get_from_str
from comments import dal as dal_comment
from dynamodb.types import RootItem
from events import dal as dal_event
from names import dal as dal_names
from roots import dal as dal_roots
from forces import dal as dal_forces


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
        dal_names.create(
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
    data_parsed: List[Any] = json.loads(json.dumps(data), parse_float=Decimal)
    coroutines.extend([
        dal_group.create(
            group,
        )
        for group in data_parsed
    ])
    return all(await collect(coroutines))


async def populate_findings(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    data_parsed: List[Any] = json.loads(json.dumps(data), parse_float=Decimal)
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


async def populate_roots(data: Tuple[Tuple[str, RootItem], ...]) -> bool:
    await collect(tuple(
        dal_roots.create_root(group_name=group_name, root=root)
        for group_name, root in data
    ))

    return True


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


async def populate_comments(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    coroutines.extend([
        dal_comment.create(
            comment['user_id'],
            comment,
        )
        for comment in data
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

async def populate_executions(data: List[Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    for execution in data:
        execution['date'] = get_from_str(execution['date'],date_format='%Y-%m-%dT%H:%M:%SZ')
    coroutines.extend([
        dal_forces.create_execution(
            **execution
        )
        for execution in data
    ])
    return all(await collect(coroutines))

async def populate(data: Dict[str, Any]) -> bool:
    coroutines: List[Awaitable[bool]] = []
    functions: Dict[str, Any] = globals()
    for name, dataset in data.items():
        coroutines.append(functions[f'populate_{name}'](dataset))
    return all(await collect(coroutines))
