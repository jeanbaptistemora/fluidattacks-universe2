# Standard
from typing import Any, Dict, Optional, Tuple

# Third party
from urllib3.util.url import parse_url, Url

# Local
from backend.dal import root as root_dal
from backend.domain import organization as org_domain
from backend.exceptions import InvalidParameter, RepeatedValues, RootNotFound
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import datetime, validations


def format_root(root: Dict[str, Any]) -> Root:
    assert root['kind'] in {'Git', 'IP', 'URL'}
    root_state: Dict[str, Any] = root['historic_state'][-1]

    if root['kind'] == 'Git':
        return GitRoot(
            branch=root['branch'],
            environment=root_state['environment'],
            environment_urls=root_state.get('environment_urls', []),
            filter=root_state.get('filter'),
            id=root['id'],
            includes_health_check=root_state['includes_health_check'],
            url=root['url']
        )

    if root['kind'] == 'IP':
        return IPRoot(
            address=root_state['address'],
            id=root['id'],
            port=root_state['port']
        )

    return URLRoot(
        host=root_state['host'],
        id=root['id'],
        path=root_state['path'],
        port=root_state['port'],
        protocol=root_state['protocol']
    )


async def get_root_by_id(root_id: str) -> Dict[str, Any]:
    root: Optional[Dict[str, Any]] = await root_dal.get_root_by_id(root_id)

    if root:
        return {
            **root,
            'group_name': root['sk'].split('GROUP#')[-1],
            'id': root['pk']
        }
    raise RootNotFound()


async def get_roots_by_group(group_name: str) -> Tuple[Dict[str, Any], ...]:
    roots = await root_dal.get_roots_by_group(group_name)

    return tuple(
        {
            **root,
            'group_name': root['pk'].split('GROUP#')[-1],
            'id': root['sk']
        }
        for root in roots
    )


def _matches_root(
    kind: str,
    root: Dict[str, Any],
    new_root: Dict[str, str]
) -> bool:
    assert kind in {'Git', 'IP', 'URL'}
    current_state: Dict[str, str] = root['historic_state'][-1]

    if kind == root['kind'] == 'Git':
        return (
            root['url'] == new_root['url']
            and root['branch'] == new_root['branch']
        )

    if kind == root['kind'] == 'IP':
        return (
            current_state['address'] == new_root['address']
            and current_state['port'] == new_root['port']
        )

    if kind == root['kind'] == 'URL':
        return (
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


async def add_git_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()

    if is_valid_git_repo(kwargs['url'], kwargs['branch']):
        kind: str = 'Git'
        org_id: str = await org_domain.get_id_for_group(group_name)
        initial_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'environment': kwargs['environment'],
            'filter': kwargs.get('filter'),
            'includes_health_check': kwargs['includes_health_check'],
            'user': user_email
        }
        root_attributes: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'historic_state': [initial_state],
            'kind': kind,
            'url': kwargs['url'],
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
    root_id: str = kwargs['root_id']
    root: Dict[str, Any] = await get_root_by_id(root_id)
    is_valid: bool = (
        is_valid_git_repo(kwargs['url'], kwargs['branch'])
        and root['kind'] == 'Git'
    )

    if is_valid:
        group_name: str = root['group_name']
        new_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'environment': kwargs['environment'],
            'filter': kwargs.get('filter'),
            'includes_health_check': kwargs['includes_health_check'],
            'user': user_email
        }

        await root_dal.update(
            group_name,
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
    else:
        raise InvalidParameter()
