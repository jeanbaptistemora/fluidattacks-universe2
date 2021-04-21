# Standard
import re
from typing import Any, List, Optional, Tuple
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
    HasOpenVulns,
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
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
            address=root.metadata.address,
            id=root.id,
            port=root.metadata.port
        )

    return URLRoot(
        host=root.metadata.host,
        id=root.id,
        path=root.metadata.path,
        port=root.metadata.port,
        protocol=root.metadata.protocol
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

    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname,
        await get_roots(group_name=group_name)
    )

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
            new_repo=None,
            nickname=nickname,
            reason=None,
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
        metadata=IPRootMetadata(
            address=address,
            port=port,
            type='IP'
        ),
        state=IPRootState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            new_repo=None,
            reason=None,
            status='ACTIVE'
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
        metadata=URLRootMetadata(
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            type='URL'
        ),
        state=URLRootState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            new_repo=None,
            reason=None,
            status='ACTIVE'
        )
    )
    await roots_dal.create_root(root=root)


def _format_root_nickname(nickname: str, url: str) -> str:
    nick = unquote(url).split('/')[-1]
    if nickname:
        nick = unquote(nickname)
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

    await roots_dal.update_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            environment_urls=environment_urls,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            new_repo=None,
            nickname=root.state.nickname,
            reason=None,
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

    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname,
        await get_roots(group_name=group_name),
        old_nickname=root.state.nickname
    )

    await roots_dal.update_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            environment_urls=root.state.environment_urls,
            environment=kwargs['environment'],
            gitignore=gitignore,
            includes_health_check=kwargs['includes_health_check'],
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            new_repo=None,
            nickname=nickname,
            reason=None,
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


async def _has_open_vulns(root: GitRootItem) -> bool:
    return await roots_dal.has_open_vulns(nickname=root.state.nickname)


async def activate_root(
    *,
    context: Any,
    group_name: str,
    root_id: str,
    user_email: str
) -> None:
    new_status = 'ACTIVE'
    root = await get_root(group_name=group_name, root_id=root_id)

    if root.state.status != new_status:
        group_loader: DataLoader = context.group_all
        group = await group_loader.load(group_name)
        org_roots = await get_org_roots(org_id=group['organization'])

        if isinstance(root, GitRootItem):
            if not validations.is_git_unique(
                root.metadata.url,
                root.metadata.branch,
                org_roots
            ):
                raise RepeatedRoot()

            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=GitRootState(
                    environment_urls=root.state.environment_urls,
                    environment=root.state.environment,
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=None,
                    nickname=root.state.nickname,
                    reason=None,
                    status=new_status
                )
            )

            if root.state.includes_health_check:
                await notifications_domain.request_health_check(
                    branch=root.metadata.branch,
                    group_name=group_name,
                    repo_url=root.metadata.url,
                    requester_email=user_email,
                )

        if isinstance(root, IPRootItem):
            if not validations.is_ip_unique(
                root.metadata.address,
                root.metadata.port,
                org_roots
            ):
                raise RepeatedRoot()

            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=IPRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=None,
                    reason=None,
                    status=new_status
                )
            )

        if isinstance(root, URLRootItem):
            if not validations.is_url_unique(
                root.metadata.host,
                root.metadata.path,
                root.metadata.port,
                root.metadata.protocol,
                org_roots
            ):
                raise RepeatedRoot()

            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=URLRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=None,
                    reason=None,
                    status=new_status
                )
            )


async def deactivate_root(
    *,
    group_name: str,
    new_repo: Optional[str],
    reason: str,
    root_id: str,
    user_email: str
) -> None:
    new_status = 'INACTIVE'
    root = await get_root(group_name=group_name, root_id=root_id)
    repo = new_repo if reason == 'MOVED_TO_ANOTHER_REPO' else None

    if root.state.status != new_status:
        if isinstance(root, GitRootItem):
            if await _has_open_vulns(root=root):
                raise HasOpenVulns()

            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=GitRootState(
                    environment_urls=root.state.environment_urls,
                    environment=root.state.environment,
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=repo,
                    nickname=root.state.nickname,
                    reason=reason,
                    status=new_status
                )
            )

            if root.state.includes_health_check:
                await notifications_domain.cancel_health_check(
                    branch=root.metadata.branch,
                    group_name=group_name,
                    repo_url=root.metadata.url,
                    requester_email=user_email
                )

        if isinstance(root, IPRootItem):
            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=IPRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=repo,
                    reason=reason,
                    status=new_status
                )
            )

        if isinstance(root, URLRootItem):
            await roots_dal.update_root_state(
                group_name=group_name,
                root_id=root_id,
                state=URLRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    new_repo=repo,
                    reason=reason,
                    status=new_status
                )
            )


async def update_root_state(
    context: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    state: str
) -> None:
    if state == 'ACTIVE':
        await activate_root(
            context=context,
            group_name=group_name,
            root_id=root_id,
            user_email=user_email
        )
    else:
        await deactivate_root(
            group_name=group_name,
            new_repo=None,
            reason='UNKNOWN',
            root_id=root_id,
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
            and root.state.status == 'ACTIVE'
        )
    except StopIteration:
        raise RootNotFound()
