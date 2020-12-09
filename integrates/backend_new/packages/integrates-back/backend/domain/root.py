# Standard
import re
from typing import Any, Dict, Optional, Tuple

# Third party
from urllib.parse import unquote
from urllib3.util.url import parse_url, Url

# Local
from backend import authz
from backend.dal import root as root_dal
from backend.domain import organization as org_domain
from backend.exceptions import (
    InvalidParameter,
    PermissionDenied,
    RepeatedValues,
    RootNotFound
)
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import datetime, validations


def format_root(root: Dict[str, Any]) -> Root:
    root_state: Dict[str, Any] = root['historic_state'][-1]

    if root['kind'] == 'Git':
        return GitRoot(
            branch=root['branch'],
            environment=root_state['environment'],
            environment_urls=root_state.get('environment_urls', []),
            filter=root_state.get('filter'),
            id=root['sk'],
            includes_health_check=root_state['includes_health_check'],
            state=root_state['state'],
            url=root['url']
        )

    if root['kind'] == 'IP':
        return IPRoot(
            address=root_state['address'],
            id=root['sk'],
            port=root_state['port']
        )

    return URLRoot(
        host=root_state['host'],
        id=root['sk'],
        path=root_state['path'],
        port=root_state['port'],
        protocol=root_state['protocol']
    )


def _is_active(root: Dict[str, Any]) -> bool:
    state: str = root['historic_state'][-1]['state']
    return state == 'ACTIVE'


async def get_root_by_id(root_id: str) -> Dict[str, Any]:
    root: Optional[Dict[str, Any]] = await root_dal.get_root_by_id(root_id)

    if root:
        return {
            **root,
            'group_name': root['pk'].split('GROUP#')[-1],
        }
    raise RootNotFound()


async def get_roots_by_group(group_name: str) -> Tuple[Dict[str, Any], ...]:
    roots: Tuple[Dict[str, Any], ...] = await root_dal.get_roots_by_group(
        group_name
    )

    return tuple(
        {
            **root,
            'group_name': root['pk'].split('GROUP#')[-1],
        }
        for root in roots
    )


def _matches_root(
    kind: str,
    root: Dict[str, Any],
    new_root: Dict[str, Any]
) -> bool:
    current_state: Dict[str, str] = root['historic_state'][-1]

    if kind == root['kind'] == 'Git':
        return bool(
            root['url'] == new_root['url']
            and root['branch'] == new_root['branch']
        )

    if kind == root['kind'] == 'IP':
        return bool(
            current_state['address'] == new_root['address']
            and current_state['port'] == new_root['port']
        )

    if kind == root['kind'] == 'URL':
        return bool(
            current_state['host'] == new_root['host']
            and current_state['path'] == new_root['path']
            and current_state['port'] == new_root['port']
            and current_state['protocol'] == new_root['protocol']
        )

    return False


async def _is_unique_in_org(
    org_id: str,
    kind: str,
    new_root: Dict[str, Any]
) -> bool:
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)

    for group_name in org_groups:
        group_roots = await get_roots_by_group(group_name)

        if next(
            (
                root
                for root in group_roots
                if _matches_root(kind, root, new_root)
            ),
            None
        ):
            return False

    return True


def is_valid_git_repo(url: str, branch: str) -> bool:
    return (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    )


def format_git_repo_url(raw_url: str) -> str:
    is_ssh: bool = (
        raw_url.startswith('ssh://')
        or bool(re.match(r'^\w+@.*', raw_url))
    )
    url = (
        f'ssh://{raw_url}'
        if is_ssh and not raw_url.startswith('ssh://')
        else raw_url
    )

    return unquote(url)


async def add_git_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()
    url: str = format_git_repo_url(kwargs['url'])

    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        kwargs.get('filter')
        and not enforcer(group_name, 'update_git_root_filter')
    ):
        raise PermissionDenied()

    if is_valid_git_repo(url, kwargs['branch']):
        kind: str = 'Git'
        org_id: str = await org_domain.get_id_for_group(group_name)
        initial_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'environment': kwargs['environment'],
            'filter': kwargs.get('filter'),
            'includes_health_check': kwargs['includes_health_check'],
            'state': 'ACTIVE',
            'user': user_email
        }
        root_attributes: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'historic_state': [initial_state],
            'kind': kind,
            'url': url
        }

        if await _is_unique_in_org(org_id, kind, root_attributes):
            await root_dal.create(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


async def add_ip_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()
    is_valid: bool = (
        validations.is_valid_ip(kwargs['address'])
        and 0 <= int(kwargs['port']) <= 65535
    )

    if is_valid:
        kind: str = 'IP'
        org_id: str = await org_domain.get_id_for_group(group_name)
        initial_state: Dict[str, Any] = {
            'address': kwargs['address'],
            'date': datetime.get_as_str(datetime.get_now()),
            'port': kwargs['port'],
            'user': user_email
        }

        if await _is_unique_in_org(org_id, kind, initial_state):
            root_attributes: Dict[str, Any] = {
                'historic_state': [initial_state],
                'kind': kind
            }
            await root_dal.create(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


async def add_url_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()
    url_attributes: Url = parse_url(kwargs['url'])
    is_valid: bool = (
        validations.is_valid_url(kwargs['url'])
        and url_attributes.scheme in {'http', 'https'}
    )

    if is_valid:
        default_port: int = 443 if url_attributes.scheme == 'https' else 80
        kind: str = 'URL'
        org_id: str = await org_domain.get_id_for_group(group_name)
        initial_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'host': url_attributes.host,
            'path': url_attributes.path or '/',
            'port': url_attributes.port or default_port,
            'protocol': url_attributes.scheme.upper(),
            'user': user_email
        }

        if await _is_unique_in_org(org_id, kind, initial_state):
            root_attributes: Dict[str, Any] = {
                'historic_state': [initial_state],
                'kind': kind
            }
            await root_dal.create(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


async def update_git_root(user_email: str, **kwargs: Any) -> None:
    root_id: str = kwargs['id']
    root: Dict[str, Any] = await get_root_by_id(root_id)
    is_valid: bool = (
        _is_active(root)
        and is_valid_git_repo(root['url'], root['branch'])
        and root['kind'] == 'Git'
    )

    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        kwargs.get('filter') != root['historic_state'][-1].get('filter')
        and not enforcer(root['group_name'], 'update_git_root_filter')
    ):
        raise PermissionDenied()

    if is_valid:
        group_name: str = root['group_name']
        new_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'environment': kwargs['environment'],
            'filter': kwargs.get('filter'),
            'includes_health_check': kwargs['includes_health_check'],
            'state': 'ACTIVE',
            'user': user_email
        }

        await root_dal.update(
            group_name,
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
    else:
        raise InvalidParameter()


async def update_root_state(user_email: str, root_id: str, state: str) -> None:
    root: Dict[str, Any] = await get_root_by_id(root_id)
    last_state: Dict[str, Any] = root['historic_state'][-1]

    if last_state['state'] != state:
        new_state: Dict[str, Any] = {
            **last_state,
            'date': datetime.get_as_str(datetime.get_now()),
            'state': state,
            'user': user_email
        }

        await root_dal.update(
            root['group_name'],
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
