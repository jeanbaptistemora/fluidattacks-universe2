# Standard
from typing import Any, Dict, Tuple

# Third party
from urllib3.util.url import parse_url, Url

# Local
from backend.dal import root as root_dal
from backend.domain import organization as org_domain
from backend.exceptions import InvalidParameter, RepeatedValues
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import datetime, validations


def format_root(root: Dict[str, Any]) -> Root:
    assert root['kind'] in {'Git', 'IP', 'URL'}
    root_state: Dict[str, Any] = root['historic_state'][-1]

    if root['kind'] == 'Git':
        return GitRoot(
            branch=root_state['branch'],
            directory_filtering=root_state.get('directory_filtering'),
            environment=root_state['environment'],
            id=root['sk'],
            url=root_state['url']
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


async def get_roots_by_group(group_name: str) -> Tuple[Root, ...]:
    roots = await root_dal.get_roots_by_group(group_name)

    return tuple(format_root(root) for root in roots)


async def _is_unique_in_org(
    org_id: str,
    kind: str,
    new_root: Dict[str, Any]
) -> bool:
    assert kind in {'Git', 'IP', 'URL'}
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)

    for group_name in org_groups:
        group_roots: Tuple[Root, ...] = await get_roots_by_group(group_name)

        if kind == 'Git' and bool(next(
            (
                root
                for root in group_roots
                if isinstance(root, GitRoot)
                and root.url == new_root['url']
                and root.branch == new_root['branch']
            ),
            None
        )):
            return False

        if kind == 'IP' and bool(next(
            (
                root
                for root in group_roots
                if isinstance(root, IPRoot)
                and root.address == new_root['address']
                and root.port == new_root['port']
            ),
            None
        )):
            return False

        if kind == 'URL' and bool(next(
            (
                root
                for root in group_roots
                if isinstance(root, URLRoot)
                and root.host == new_root['host']
                and root.path == new_root['path']
                and root.port == new_root['port']
                and root.protocol == new_root['protocol']
            ),
            None
        )):
            return False

    return True


async def add_git_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()
    is_valid_repo: bool = (
        validations.is_valid_url(kwargs['url'])
        and validations.is_valid_git_branch(kwargs['branch'])
    )
    is_valid_env: bool = (
        validations.is_valid_url(kwargs['environment']['url'])
        if kwargs['environment'].get('url')
        else True
    )

    if is_valid_repo and is_valid_env:
        kind: str = 'Git'
        org_id: str = await org_domain.get_id_for_group(group_name)
        initial_state: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'date': datetime.get_as_str(datetime.get_now()),
            'directory_filtering': kwargs.get('directory_filtering'),
            'environment': kwargs.get('environment'),
            'url': kwargs['url'],
            'user': user_email
        }

        if await _is_unique_in_org(org_id, kind, initial_state):
            root_attributes: Dict[str, Any] = {
                'historic_state': [initial_state],
                'kind': kind
            }
            await root_dal.add_root(group_name, root_attributes)
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
            await root_dal.add_root(group_name, root_attributes)
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
            await root_dal.add_root(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()
