"""
This migration moves items from fi_roots to the new single-table
integrates_vms

Execution Time:
Finalization Time:
"""
# Standard libraries
import time
from datetime import timezone
from typing import Any, Dict, List

# Third party libraries
from aioextensions import collect, run
from boto3.dynamodb.conditions import Attr

# Local libraries
from backend.dal.helpers import dynamodb
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState
)
from newutils import datetime as datetime_utils
from roots import dal as roots_dal


def _convert_to_iso(date: str) -> str:
    utc = datetime_utils.get_from_str(date).astimezone(tz=timezone.utc)
    iso: str = utc.isoformat()

    return iso


async def _migrate_cloning(
    cloning: List[Dict[str, Any]],
    group_name: str,
    root_id: str
) -> None:
    await collect(tuple(
        roots_dal.update_git_root_cloning(
            cloning=GitRootCloning(
                modified_date=_convert_to_iso(item['date']),
                reason=item['message'],
                status=item['status']
            ),
            group_name=group_name,
            root_id=root_id
        )
        for item in cloning[1:-1]
    ))

    await roots_dal.update_git_root_cloning(
        cloning=GitRootCloning(
            modified_date=_convert_to_iso(cloning[-1]['date']),
            reason=cloning[-1]['message'],
            status=cloning[-1]['status']
        ),
        group_name=group_name,
        root_id=root_id
    )


async def _migrate_state(
    group_name: str,
    root_id: str,
    state: List[Dict[str, Any]]
) -> None:
    await collect(tuple(
        roots_dal.update_git_root_state(
            group_name=group_name,
            root_id=root_id,
            state=GitRootState(
                environment_urls=item['environment_urls'],
                environment=item['environment'],
                gitignore=item['gitignore'],
                includes_health_check=item['includes_health_check'],
                modified_by=item['user'],
                modified_date=_convert_to_iso(item['date']),
                nickname=item.get('nickname'),
                status=item['state']
            )
        )
        for item in state[1:-1]
    ))

    await roots_dal.update_git_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            environment_urls=state[-1]['environment_urls'],
            environment=state[-1]['environment'],
            gitignore=state[-1]['gitignore'],
            includes_health_check=state[-1]['includes_health_check'],
            modified_by=state[-1]['user'],
            modified_date=_convert_to_iso(state[-1]['date']),
            nickname=state[-1].get('nickname'),
            status=state[-1]['state']
        )
    )


async def _migrate_root(legacy_root: Dict[str, Any]) -> None:
    group_name = legacy_root['pk'].split('#')[1]
    root_id = legacy_root['sk'].split('#')[1]
    cloning = legacy_root['historic_cloning_status']
    state = legacy_root['historic_state']
    root = GitRootItem(
        cloning=GitRootCloning(
            modified_date=_convert_to_iso(cloning[0]['date']),
            reason=cloning[0]['message'],
            status=cloning[0]['status']
        ),
        id=root_id,
        metadata=GitRootMetadata(
            branch=legacy_root['branch'],
            type=legacy_root['kind'],
            url=legacy_root['url']
        ),
        state=GitRootState(
            environment_urls=state[0]['environment_urls'],
            environment=state[0]['environment'],
            gitignore=state[0]['gitignore'],
            includes_health_check=state[0]['includes_health_check'],
            modified_by=state[0]['user'],
            modified_date=_convert_to_iso(state[0]['date']),
            nickname=state[0].get('nickname'),
            status=state[0]['state']
        )
    )

    await roots_dal.create_git_root(group_name=group_name, root=root)
    await _migrate_cloning(cloning, group_name, root_id)
    await _migrate_state(group_name, root_id, state)


async def main() -> None:
    legacy_roots = await dynamodb.async_scan(
        'fi_roots',
        {'FilterExpression': Attr('kind').eq('Git')}
    )
    print('[INFO] Will migrate', len(legacy_roots), 'roots')
    await collect(tuple(_migrate_root(root) for root in legacy_roots))


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
