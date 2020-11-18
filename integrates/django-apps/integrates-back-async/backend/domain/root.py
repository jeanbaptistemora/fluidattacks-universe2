# Standard
from typing import Any, Dict, List

# Third party
from urllib3.util.url import parse_url, Url

# Local
from backend.dal import root as root_dal
from backend.exceptions import InvalidParameter
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import validations


async def get_roots_by_group(group_name: str) -> List[Root]:
    roots = await root_dal.get_roots_by_group(group_name)

    return [
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
    ]


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
        root_attributes: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'directory_filtering': kwargs.get('directory_filtering'),
            'environment': kwargs.get('environment'),
            'created_by': user_email,
            'kind': 'Git',
            'url': kwargs['url']
        }

        await root_dal.add_root(group_name, root_attributes)
    else:
        raise InvalidParameter()


async def add_ip_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()
    is_valid: bool = (
        validations.is_valid_ip(kwargs['address'])
        and 0 <= int(kwargs['port']) <= 65535
    )

    if is_valid:
        root_attributes: Dict[str, Any] = {
            'address': kwargs['address'],
            'created_by': user_email,
            'kind': 'IP',
            'port': kwargs['port']
        }

        await root_dal.add_root(group_name, root_attributes)
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
        root_attributes: Dict[str, Any] = {
            'created_by': user_email,
            'host': url_attributes.host,
            'kind': 'URL',
            'path': url_attributes.path or '/',
            'port': url_attributes.port or default_port,
            'protocol': url_attributes.scheme.upper()
        }

        await root_dal.add_root(group_name, root_attributes)
    else:
        raise InvalidParameter()
