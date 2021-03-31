# Standard
import re
from typing import (
    Any,
    List,
    Tuple,
)
from urllib.parse import unquote
from uuid import uuid4

# Third party
import newrelic.agent
from aiodataloader import DataLoader
from aioextensions import collect
from urllib3.util.url import parse_url

# Local
from backend import authz
from backend.exceptions import (
    InvalidChar,
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RepeatedRootNickname,
    RepeatedValues,
    RootNotFound
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
    validations as validation_utils
)
from notifications import domain as notifications_domain
from organizations import domain as orgs_domain
from roots import (
    dal as roots_dal,
    validations,
)
from roots.types import (
    GitRoot,
    GitRootCloningStatus,
    IPRoot,
    Root,
    URLRoot,
)


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
            group_name=root.group_name,
            id=root.id,
            includes_health_check=root.state.includes_health_check,
            last_cloning_status_update=root.cloning.modified_date,
            last_state_status_update=root.state.modified_date,
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
    root = await roots_dal.get_root(group_name=group_name, root_id=root_id)

    if root:
        return root

    raise RootNotFound()


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await roots_dal.get_roots(group_name=group_name)


@newrelic.agent.function_trace()
async def get_org_roots(*, org_id: str) -> Tuple[RootItem, ...]:
    org_groups = await orgs_domain.get_groups(org_id)

    return tuple(
        root
        for group_roots in await collect(tuple(
            get_roots(group_name=group_name)
            for group_name in org_groups
        ))
        for root in group_roots
    )


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
    nickname: str = _format_root_nickname(kwargs.get('nickname', ''), url)

    gitignore = kwargs['gitignore']
    enforcer = await authz.get_group_level_enforcer(user_email)
    if not validations.validate_nickname(nickname):
        raise InvalidChar()
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

    if not validations.is_nickname_unique(
        nickname,
        await get_roots(group_name=group_name)
    ):
        raise RepeatedRootNickname()

    group = await group_loader.load(group_name)
    if not validations.is_git_unique(
        url,
        branch,
        await get_org_roots(org_id=group['organization'])
    ):
        raise RepeatedRoot()

    root = GitRootItem(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason='root created',
            status='UNKNOWN'
        ),
        group_name=group_name,
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
    await roots_dal.create_root(root=root)

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

    if not validations.is_ip_unique(
        address,
        port,
        await get_org_roots(org_id=group['organization'])
    ):
        raise RepeatedValues()

    root = IPRootItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=IPRootMetadata(type='IP'),
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            port=port
        )
    )
    await roots_dal.create_root(root=root)


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

    if not validations.is_url_unique(
        host,
        path,
        port,
        protocol,
        await get_org_roots(org_id=group['organization'])
    ):
        raise RepeatedValues()

    root = URLRootItem(
        group_name=group_name,
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
    await roots_dal.create_root(root=root)


def _format_root_nickname(nickname: str, url: str) -> str:
    nick = url.split('/')[-1]
    if nickname:
        nick = nickname
    # Return the repo name as nickname
    if nick.endswith('.git'):
        return nick[:-4]
    return nick


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

    nickname = _format_root_nickname(
        kwargs.get('nickname', ''),
        root.state.nickname
    )

    if not validations.validate_nickname(nickname):
        raise InvalidChar()

    if (
        nickname != root.state.nickname
        and not validations.is_nickname_unique(
            nickname,
            await get_roots(group_name=group_name)
        )
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
            nickname=nickname,
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


async def update_root_cloning_status(
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> None:
    validation_utils.validate_field_length(message, 400)
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


async def update_root_state(
    context: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    state: str
) -> None:
    root = await get_root(group_name=group_name, root_id=root_id)

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    if root.state.status != state:
        group_loader: DataLoader = context.group_all
        group = await group_loader.load(group_name)
        if (
            state == 'ACTIVE'
            and not validations.is_git_unique(
                root.metadata.url,
                root.metadata.branch,
                await get_org_roots(org_id=group['organization'])
            )
        ):
            raise RepeatedRoot()

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


def get_root_id_by_filename(
    filename: str,
    group_roots: Tuple[Root, ...]
) -> str:
    root_nickname = filename.split('/')[0]
    file_name_root_ids = [
        root.id
        for root in group_roots
        if isinstance(root, GitRoot)
        and root.nickname == root_nickname
    ]

    if not file_name_root_ids:
        raise RootNotFound()

    return file_name_root_ids[0]


async def get_root_by_nickname(
    *,
    group_name: str,
    repo_nickname: str
) -> GitRootItem:
    try:
        return next(
            root
            for root in await get_roots(group_name=group_name)
            if isinstance(root, GitRootItem)
            and root.state.nickname == repo_nickname
        )
    except StopIteration:
        raise RootNotFound()
