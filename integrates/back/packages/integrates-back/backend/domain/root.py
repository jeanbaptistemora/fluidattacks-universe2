# Standard
import re
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)
from urllib.parse import unquote

# Third party
import newrelic.agent
from aioextensions import collect
from urllib3.util.url import parse_url, Url

# Local
from backend import authz
from backend.dal import root as root_dal
from backend.domain import (
    notifications as notifications_domain,
    organization as org_domain
)
from backend.exceptions import (
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RepeatedValues,
    RootNotFound
)
from backend.typing import (
    GitRoot,
    GitRootCloningStatus,
    IPRoot,
    URLRoot,
    Root,
)
from backend.utils import validations
from newutils import datetime


def format_root(root: Dict[str, Any]) -> Root:
    root_state: Dict[str, Any] = root['historic_state'][-1]

    if root['kind'] == 'Git':
        cloning_status: Dict[str, Any] = root['historic_cloning_status'][-1]

        return GitRoot(
            branch=root['branch'],
            cloning_status=GitRootCloningStatus(
                status=cloning_status['status'],
                message=cloning_status['message'],
            ),
            environment=root_state['environment'],
            environment_urls=root_state['environment_urls'],
            gitignore=root_state['gitignore'],
            id=root['sk'],
            includes_health_check=root_state['includes_health_check'],
            last_status_update=root_state['date'],
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


@newrelic.agent.function_trace()  # type: ignore
async def _is_git_unique_in_org(org_id: str, url: str, branch: str) -> bool:
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)
    org_roots: Tuple[Tuple[str, str], ...] = tuple(
        (root['url'], root['branch'])
        for group_roots in await collect(
            get_roots_by_group(group_name)
            for group_name in org_groups
        )
        for root in group_roots
        if root['kind'] == 'Git'
        and root['historic_state'][-1]['state'] == 'ACTIVE'
    )

    return (url, branch) not in org_roots


def _format_git_repo_url(raw_url: str) -> str:
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


async def add_git_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    url: str = _format_git_repo_url(kwargs['url'])
    branch: str = kwargs['branch']
    is_valid: bool = (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    )

    gitignore = kwargs['gitignore']
    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        gitignore
        and not enforcer(group_name, 'update_git_root_filter')
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()

    now_date = datetime.get_as_str(datetime.get_now())
    initial_cloning_status: Dict[str, Any] = {
        'date': now_date,
        'status': 'UNKNOWN',
        'message': 'root created'
    }

    if is_valid:
        group = await group_loader.load(group_name)
        initial_state: Dict[str, Any] = {
            'date': now_date,
            'environment': kwargs['environment'],
            'environment_urls': [],
            'gitignore': gitignore,
            'includes_health_check': kwargs['includes_health_check'],
            'state': 'ACTIVE',
            'user': user_email
        }
        root_attributes: Dict[str, Any] = {
            'branch': branch,
            'historic_state': [initial_state],
            'historic_cloning_status': [initial_cloning_status],
            'kind': 'Git',
            'url': url
        }

        if await _is_git_unique_in_org(group['organization'], url, branch):
            await root_dal.create(group_name, root_attributes)
            if kwargs['includes_health_check']:
                await notifications_domain.request_health_check(
                    requester_email=user_email,
                    group_name=group_name,
                    repo_url=url,
                    branch=branch
                )
        else:
            raise RepeatedRoot()
    else:
        raise InvalidParameter()


@newrelic.agent.function_trace()  # type: ignore
async def _is_ip_unique_in_org(org_id: str, address: str, port: int) -> bool:
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)
    org_roots: Tuple[Tuple[str, int], ...] = tuple(
        (
            root['historic_state'][-1]['address'],
            root['historic_state'][-1]['port']
        )
        for group_roots in await collect(
            get_roots_by_group(group_name)
            for group_name in org_groups
        )
        for root in group_roots
        if root['kind'] == 'IP'
    )

    return (address, port) not in org_roots


async def add_ip_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    address: str = kwargs['address']
    port: int = kwargs['port']
    is_valid: bool = (
        validations.is_valid_ip(address)
        and 0 <= int(port) <= 65535
    )

    if is_valid:
        group = await group_loader.load(group_name)
        org_id = group['organization']
        initial_state: Dict[str, Any] = {
            'address': address,
            'date': datetime.get_as_str(datetime.get_now()),
            'port': port,
            'user': user_email
        }

        if await _is_ip_unique_in_org(org_id, address, port):
            root_attributes: Dict[str, Any] = {
                'historic_state': [initial_state],
                'kind': 'IP'
            }
            await root_dal.create(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


@newrelic.agent.function_trace()  # type: ignore
async def _is_url_unique_in_org(
    org_id: str,
    host: str,
    path: str,
    port: int,
    protocol: str
) -> bool:
    org_groups: Tuple[str, ...] = await org_domain.get_groups(org_id)
    org_roots: Tuple[Tuple[str, str, int, str], ...] = tuple(
        (
            root['historic_state'][-1]['host'],
            root['historic_state'][-1]['path'],
            root['historic_state'][-1]['port'],
            root['historic_state'][-1]['protocol']
        )
        for group_roots in await collect(
            get_roots_by_group(group_name)
            for group_name in org_groups
        )
        for root in group_roots
        if root['kind'] == 'URL'
    )

    return (host, path, port, protocol) not in org_roots


async def add_url_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    url_attributes: Url = parse_url(kwargs['url'])
    is_valid: bool = (
        validations.is_valid_url(kwargs['url'])
        and url_attributes.scheme in {'http', 'https'}
    )

    if is_valid:
        host: str = url_attributes.host
        path: str = url_attributes.path or '/'
        default_port: int = 443 if url_attributes.scheme == 'https' else 80
        port: int = url_attributes.port or default_port
        protocol: str = url_attributes.scheme.upper()
        group = await group_loader.load(group_name)

        initial_state: Dict[str, Any] = {
            'date': datetime.get_as_str(datetime.get_now()),
            'host': host,
            'path': path,
            'port': port,
            'protocol': protocol,
            'user': user_email
        }
        if await _is_url_unique_in_org(
            group['organization'],
            host,
            path,
            port,
            protocol
        ):
            root_attributes: Dict[str, Any] = {
                'historic_state': [initial_state],
                'kind': 'URL'
            }
            await root_dal.create(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


def _is_active(root: Dict[str, Any]) -> bool:
    state: str = root['historic_state'][-1]['state']
    return state == 'ACTIVE'


async def update_git_root(user_email: str, **kwargs: Any) -> None:
    root_id: str = kwargs['id']
    root: Dict[str, Any] = await get_root_by_id(root_id)
    last_state: Dict[str, Any] = root['historic_state'][-1]
    is_valid: bool = _is_active(root) and root['kind'] == 'Git'

    gitignore = kwargs['gitignore']
    filter_changed: bool = gitignore != last_state['gitignore']
    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        filter_changed
        and not enforcer(root['group_name'], 'update_git_root_filter')
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, root['url']):
        raise InvalidRootExclusion()

    if is_valid:
        group_name: str = root['group_name']
        new_state: Dict[str, Any] = {
            **last_state,
            'date': datetime.get_as_str(datetime.get_now()),
            'environment': kwargs['environment'],
            'gitignore': gitignore,
            'includes_health_check': kwargs['includes_health_check'],
            'user': user_email
        }

        await root_dal.update(
            group_name,
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
        health_check_changed: bool = (
            kwargs['includes_health_check']
            != last_state['includes_health_check']
        )
        if health_check_changed:
            if kwargs['includes_health_check']:
                await notifications_domain.request_health_check(
                    requester_email=user_email,
                    group_name=group_name,
                    repo_url=root['url'],
                    branch=root['branch']
                )
            else:
                await notifications_domain.cancel_health_check(
                    requester_email=user_email,
                    group_name=group_name,
                    repo_url=root['url'],
                    branch=root['branch']
                )
    else:
        raise InvalidParameter()


async def update_git_environments(
    user_email: str,
    root_id: str,
    environment_urls: Tuple[str, ...]
) -> None:
    root: Dict[str, Any] = await get_root_by_id(root_id)
    last_state: Dict[str, Any] = root['historic_state'][-1]
    is_valid: bool = (
        _is_active(root)
        and root['kind'] == 'Git'
        and all(validations.is_valid_url(url) for url in environment_urls)
    )

    if is_valid:
        group_name: str = root['group_name']
        new_state: Dict[str, Any] = {
            **last_state,
            'date': datetime.get_as_str(datetime.get_now()),
            'environment_urls': environment_urls,
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
            'user': user_email,
        }

        await root_dal.update(
            root['group_name'],
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
        if last_state['includes_health_check']:
            if state == 'ACTIVE':
                await notifications_domain.request_health_check(
                    requester_email=user_email,
                    group_name=root['group_name'],
                    repo_url=root['url'],
                    branch=root['branch'],
                )
            else:
                await notifications_domain.cancel_health_check(
                    requester_email=user_email,
                    group_name=root['group_name'],
                    repo_url=root['url'],
                    branch=root['branch'],
                )


async def update_root_cloning_status(
    root_id: str,
    status: str,
    message: str,
) -> None:
    validations.validate_field_length(message, 400)
    root: Dict[str, Any] = await get_root_by_id(root_id)
    last_status = root['historic_cloning_status'][-1]

    if last_status['status'] != status:
        new_status: Dict[str, Any] = {
            'status': status,
            'date': datetime.get_as_str(datetime.get_now()),
            'message': message,
        }

        await root_dal.update(
            root['group_name'], root_id, {
                'historic_cloning_status':
                [*root['historic_cloning_status'], new_status]
            })
