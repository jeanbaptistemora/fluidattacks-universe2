# Standard
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote
from uuid import uuid4

# Third party
import newrelic.agent
from aioextensions import collect
from urllib3.util.url import parse_url, Url

# Local
from backend import authz
from backend.domain import organization as org_domain
from backend.exceptions import (
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RepeatedRootNickname,
    RepeatedValues,
    RootNotFound
)
from backend.typing import (
    GitRoot,
    GitRootCloningStatus,
    IPRoot,
    URLRoot,
    Root
)
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    RootItem,
    URLRootItem,
    URLRootMetadata,
    URLRootState
)
from newutils import (
    datetime as datetime_utils,
    validations,
)
from notifications import domain as notifications_domain
from roots import dal as roots_dal


def format_root(root: RootItem) -> Root:
    if isinstance(root, GitRootItem):
        return GitRoot(
            branch=root.metadata.branch,
            cloning_status=GitRootCloningStatus(
                status=root.cloning.status,
                message=root.cloning.reason,
            ),
            environment=root.state.environment,
            environment_urls=root.state.environment_urls,
            gitignore=root.state.gitignore,
            id=root.id,
            includes_health_check=root.state.includes_health_check,
            last_status_update=root.state.modified_date,
            nickname=root.state.nickname,
            state=root.state.status,
            url=root.metadata.url
        )

    if isinstance(root, IPRootItem):
        return IPRoot(
            address=root.state.address,
            id=root.id,
            port=root.state.port
        )

    return URLRoot(
        host=root.state.host,
        id=root.id,
        path=root.state.path,
        port=root.state.port,
        protocol=root.state.protocol
    )


async def get_root(*, group_name: str, root_id: str) -> RootItem:
    # Temporarily needed for backwards compatibility
    r_id = root_id.split('#')[1] if root_id.startswith('ROOT#') else root_id

    root = await roots_dal.get_root(group_name=group_name, root_id=r_id)

    if root:
        return root

    raise RootNotFound()


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await roots_dal.get_roots(group_name=group_name)


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


def _is_active(root: Dict[str, Any]) -> bool:
    state: str = root['historic_state'][-1]['state']
    return state == 'ACTIVE'


@newrelic.agent.function_trace()
async def _is_git_unique_in_org(org_id: str, url: str, branch: str) -> bool:
    org_groups = await org_domain.get_groups(org_id)
    org_roots = tuple(
        (root.metadata.url, root.metadata.branch)
        for group_roots in await collect(tuple(
            get_roots(group_name=group_name)
            for group_name in org_groups
        ))
        for root in group_roots
        if isinstance(root, GitRootItem)
        and root.state.status == 'ACTIVE'
    )

    return (url, branch) not in org_roots


@newrelic.agent.function_trace()
async def _is_ip_unique_in_org(org_id: str, address: str, port: str) -> bool:
    org_groups = await org_domain.get_groups(org_id)
    org_roots = tuple(
        (root.state.address, root.state.port)
        for group_roots in await collect(
            get_roots(group_name=group_name)
            for group_name in org_groups
        )
        for root in group_roots
        if isinstance(root, IPRootItem)
    )

    return (address, port) not in org_roots


@newrelic.agent.function_trace()
async def _is_nickname_unique_in_group(group_name: str, nickname: str) -> bool:
    group_roots = await get_roots(group_name=group_name)
    nickname_roots = {
        root.state.nickname
        for root in group_roots
        if isinstance(root, GitRootItem)
    }

    return nickname not in nickname_roots


@newrelic.agent.function_trace()
async def _is_url_unique_in_org_legacy(
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


@newrelic.agent.function_trace()
async def _is_url_unique_in_org(
    org_id: str,
    host: str,
    path: str,
    port: str,
    protocol: str
) -> bool:
    org_groups = await org_domain.get_groups(org_id)
    org_roots = tuple(
        (
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol
        )
        for group_roots in await collect(
            get_roots(group_name=group_name)
            for group_name in org_groups
        )
        for root in group_roots
        if isinstance(root, URLRootItem)
    )

    return (host, path, port, protocol) not in org_roots


async def _notify_health_check(
    *,
    group_name: str,
    request: bool,
    root: GitRootItem,
    user_email: str
) -> None:
    if request:
        await notifications_domain.request_health_check(
            branch=root.metadata.branch,
            group_name=group_name,
            repo_url=root.metadata.url,
            requester_email=user_email,
        )
    else:
        await notifications_domain.cancel_health_check(
            branch=root.metadata.branch,
            group_name=group_name,
            repo_url=root.metadata.url,
            requester_email=user_email,
        )


async def add_git_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    url: str = _format_git_repo_url(kwargs['url'])
    branch: str = kwargs['branch']
    nickname: str = format_root_nickname(kwargs.get('nickname', ''), url)

    gitignore = kwargs['gitignore']
    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        gitignore
        and not enforcer(group_name, 'update_git_root_filter')
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()

    if not (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()

    if not await _is_nickname_unique_in_group(group_name, nickname):
        raise RepeatedRootNickname()

    group = await group_loader.load(group_name)
    if not await _is_git_unique_in_org(group['organization'], url, branch):
        raise RepeatedRoot()

    root = GitRootItem(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason='root created',
            status='UNKNOWN'
        ),
        id=str(uuid4()),
        metadata=GitRootMetadata(
            branch=branch,
            type='Git',
            url=url
        ),
        state=GitRootState(
            environment_urls=list(),
            environment=kwargs['environment'],
            gitignore=gitignore,
            includes_health_check=kwargs['includes_health_check'],
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            status='ACTIVE'
        )
    )
    await roots_dal.create_root(group_name=group_name, root=root)

    if kwargs['includes_health_check']:
        await _notify_health_check(
            group_name=group_name,
            request=True,
            root=root,
            user_email=user_email
        )


async def add_ip_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    address: str = kwargs['address']
    port = str(kwargs['port'])
    is_valid: bool = (
        validations.is_valid_ip(address)
        and 0 <= int(port) <= 65535
    )

    if not is_valid:
        raise InvalidParameter()

    group = await group_loader.load(group_name)
    org_id = group['organization']

    if not await _is_ip_unique_in_org(org_id, address, port):
        raise RepeatedValues()

    root = IPRootItem(
        id=str(uuid4()),
        metadata=IPRootMetadata(type='IP'),
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            port=port
        )
    )
    await roots_dal.create_root(group_name=group_name, root=root)


async def add_url_root_legacy(
    context: Any,
    user_email: str,
    **kwargs: Any
) -> None:
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
            'date': datetime_utils.get_as_str(datetime_utils.get_now()),
            'host': host,
            'path': path,
            'port': port,
            'protocol': protocol,
            'user': user_email
        }
        if await _is_url_unique_in_org_legacy(
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
            await roots_dal.create_legacy(group_name, root_attributes)
        else:
            raise RepeatedValues()
    else:
        raise InvalidParameter()


async def add_url_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group_all
    group_name: str = kwargs['group_name'].lower()
    url_attributes = parse_url(kwargs['url'])
    is_valid = (
        validations.is_valid_url(kwargs['url'])
        and url_attributes.scheme in {'http', 'https'}
    )

    if not is_valid:
        raise InvalidParameter()

    host: str = url_attributes.host
    path: str = url_attributes.path or '/'
    default_port = '443' if url_attributes.scheme == 'https' else '80'
    port = str(url_attributes.port) or default_port
    protocol: str = url_attributes.scheme.upper()
    group = await group_loader.load(group_name)

    if not await _is_url_unique_in_org(
        group['organization'],
        host,
        path,
        port,
        protocol
    ):
        raise RepeatedValues()

    root = URLRootItem(
        id=str(uuid4()),
        metadata=URLRootMetadata(type='URL'),
        state=URLRootState(
            host=host,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            path=path,
            port=port,
            protocol=protocol
        )
    )
    await roots_dal.create_root(group_name=group_name, root=root)


def format_root_legacy(root: Dict[str, Any]) -> Root:
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
            nickname=root.get('nickname', ''),
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


def format_root_nickname(nickname: str, url: str) -> str:
    nick = url.split('/')[-1]
    if nickname:
        nick = nickname
    # Return the repo name as nickname
    if nick.endswith('.git'):
        return nick[:-4]
    return nick


async def get_root_by_id(group_name: str, root_id: str) -> Dict[str, Any]:
    root: Optional[Dict[str, Any]] = await roots_dal.get_root_by_id_legacy(
        group_name,
        root_id
    )

    if root:
        return root
    raise RootNotFound()


async def get_roots_by_group(group_name: str) -> Tuple[Dict[str, Any], ...]:
    roots: Tuple[Dict[str, Any], ...] = await roots_dal\
        .get_roots_by_group_legacy(group_name)

    return tuple(
        {
            **root,
            'group_name': root['pk'].split('GROUP#')[-1],
        }
        for root in roots
    )


async def update_git_environments_legacy(
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: Tuple[str, ...]
) -> None:
    root: Dict[str, Any] = await get_root_by_id(group_name, root_id)
    last_state: Dict[str, Any] = root['historic_state'][-1]
    is_valid: bool = (
        _is_active(root)
        and root['kind'] == 'Git'
        and all(validations.is_valid_url(url) for url in environment_urls)
    )

    if is_valid:
        new_state: Dict[str, Any] = {
            **last_state,
            'date': datetime_utils.get_as_str(datetime_utils.get_now()),
            'environment_urls': environment_urls,
            'user': user_email
        }

        await roots_dal.update_legacy(
            group_name,
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
    else:
        raise InvalidParameter()


async def update_git_environments(
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: List[str]
) -> None:
    root = await get_root(group_name=group_name, root_id=root_id)

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    is_valid: bool = (
        root.state.status == 'ACTIVE'
        and all(validations.is_valid_url(url) for url in environment_urls)
    )
    if not is_valid:
        raise InvalidParameter()

    await roots_dal.update_git_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            environment_urls=environment_urls,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=root.state.nickname,
            status=root.state.status
        )
    )


async def update_git_root(user_email: str, **kwargs: Any) -> None:
    root_id: str = kwargs['id']
    group_name: str = kwargs['group_name']
    root = await get_root(group_name=group_name, root_id=root_id)

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    gitignore = kwargs['gitignore']
    filter_changed: bool = gitignore != root.state.gitignore
    enforcer = await authz.get_group_level_enforcer(user_email)
    if (
        filter_changed
        and not enforcer(group_name, 'update_git_root_filter')
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, root.metadata.url):
        raise InvalidRootExclusion()

    if root.state.status != 'ACTIVE':
        raise InvalidParameter()

    nickname = format_root_nickname(
        kwargs.get('nickname', ''),
        root.state.nickname
    )
    if (
        nickname != root.state.nickname and
        not await _is_nickname_unique_in_group(group_name, nickname)
    ):
        raise RepeatedRootNickname()

    await roots_dal.update_git_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            environment_urls=root.state.environment_urls,
            environment=kwargs['environment'],
            gitignore=gitignore,
            includes_health_check=kwargs['includes_health_check'],
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=root.state.nickname,
            status=root.state.status
        )
    )

    health_check_changed: bool = (
        kwargs['includes_health_check']
        != root.state.includes_health_check
    )
    if health_check_changed:
        await _notify_health_check(
            group_name=group_name,
            request=kwargs['includes_health_check'],
            root=root,
            user_email=user_email
        )


async def update_root_cloning_status_legacy(
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> None:
    validations.validate_field_length(message, 400)
    root: Dict[str, Any] = await get_root_by_id(group_name, root_id)
    last_status = root['historic_cloning_status'][-1]

    if last_status['status'] != status:
        new_status: Dict[str, Any] = {
            'status': status,
            'date': datetime_utils.get_as_str(datetime_utils.get_now()),
            'message': message,
        }

        await roots_dal.update_legacy(
            group_name, root_id, {
                'historic_cloning_status':
                [*root['historic_cloning_status'], new_status]
            })


async def update_root_cloning_status(
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> None:
    validations.validate_field_length(message, 400)
    root = await get_root(group_name=group_name, root_id=root_id)

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    if root.cloning.status != status:
        await roots_dal.update_git_root_cloning(
            cloning=GitRootCloning(
                modified_date=datetime_utils.get_iso_date(),
                reason=message,
                status=status
            ),
            group_name=group_name,
            root_id=root_id
        )


async def update_root_state_legacy(
    user_email: str,
    group_name: str,
    root_id: str,
    state: str
) -> None:
    root: Dict[str, Any] = await get_root_by_id(group_name, root_id)
    last_state: Dict[str, Any] = root['historic_state'][-1]

    if last_state['state'] != state:
        new_state: Dict[str, Any] = {
            **last_state,
            'date': datetime_utils.get_as_str(datetime_utils.get_now()),
            'state': state,
            'user': user_email,
        }

        await roots_dal.update_legacy(
            group_name,
            root_id,
            {'historic_state': [*root['historic_state'], new_state]}
        )
        if last_state['includes_health_check']:
            if state == 'ACTIVE':
                await notifications_domain.request_health_check(
                    requester_email=user_email,
                    group_name=group_name,
                    repo_url=root['url'],
                    branch=root['branch'],
                )
            else:
                await notifications_domain.cancel_health_check(
                    requester_email=user_email,
                    group_name=group_name,
                    repo_url=root['url'],
                    branch=root['branch'],
                )


async def update_root_state(
    user_email: str,
    group_name: str,
    root_id: str,
    state: str
) -> None:
    root = await get_root(group_name=group_name, root_id=root_id)

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    if root.state.status != state:
        await roots_dal.update_git_root_state(
            group_name=group_name,
            root_id=root_id,
            state=GitRootState(
                environment_urls=root.state.environment_urls,
                environment=root.state.environment,
                gitignore=root.state.gitignore,
                includes_health_check=root.state.includes_health_check,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                nickname=root.state.nickname,
                status=state
            )
        )

        if root.state.includes_health_check:
            await _notify_health_check(
                group_name=group_name,
                request=state == 'ACTIVE',
                root=root,
                user_email=user_email
            )
