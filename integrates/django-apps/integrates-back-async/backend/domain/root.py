# Standard
from typing import Any, Dict, Tuple

# Third party
from urllib3.util.url import parse_url, Url

# Local
from backend.dal import root as root_dal
from backend.domain import organization as org_domain
from backend.exceptions import InvalidParameter, RepeatedValues
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import validations


async def get_roots_by_group(group_name: str) -> Tuple[Root, ...]:
    roots = await root_dal.get_roots_by_group(group_name)

    return tuple(
        GitRoot(
            branch=root['branch'],
            directory_filtering=root.get('directory_filtering'),
            environment=root.get('environment'),
            id=root['sk'],
            url=root['url']
        )
        if root['kind'] == 'Git'
        else IPRoot(
            address=root['address'],
            id=root['sk'],
            port=root['port']
        )
        if root['kind'] == 'IP'
        else URLRoot(
            host=root['host'],
            id=root['sk'],
            path=root['path'],
            port=root['port'],
            protocol=root['protocol']
        )
        for root in roots
    )


async def _is_unique_in_org(org_id: str, new_root: Dict[str, Any]) -> bool:
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)

    for group_name in org_groups:
        group_roots: Tuple[Root, ...] = await get_roots_by_group(group_name)

        if new_root['kind'] == 'Git' and next(
            (
                root
                for root in group_roots
                if isinstance(root, GitRoot)
                and root.url == new_root['url']
                and root.branch == new_root['branch']
            ),
            None
        ):
            return False

        if new_root['kind'] == 'IP' and next(
            (
                root
                for root in group_roots
                if isinstance(root, IPRoot)
                and root.address == new_root['address']
                and root.port == new_root['port']
            ),
            None
        ):
            return False

        if new_root['kind'] == 'URL' and next(
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
        ):
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
        org_id: str = await org_domain.get_id_for_group(group_name)
        root_attributes: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'directory_filtering': kwargs.get('directory_filtering'),
            'environment': kwargs.get('environment'),
            'created_by': user_email,
            'kind': 'Git',
            'url': kwargs['url']
        }

        if await _is_unique_in_org(org_id, root_attributes):
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
        org_id: str = await org_domain.get_id_for_group(group_name)
        root_attributes: Dict[str, Any] = {
            'address': kwargs['address'],
            'created_by': user_email,
            'kind': 'IP',
            'port': kwargs['port']
        }

        if await _is_unique_in_org(org_id, root_attributes):
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
        org_id: str = await org_domain.get_id_for_group(group_name)
        root_attributes: Dict[str, Any] = {
            'created_by': user_email,
            'host': url_attributes.host,
            'kind': 'URL',
            'path': url_attributes.path or '/',
            'port': url_attributes.port or default_port,
            'protocol': url_attributes.scheme.upper()
        }

        if await _is_unique_in_org(org_id, root_attributes):
            await root_dal.add_root(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()
