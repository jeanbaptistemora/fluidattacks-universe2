from aiodataloader import (
    DataLoader,
)
import authz
from custom_exceptions import (
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RootNotFound,
)
from db_model import (
    roots as roots_model,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    RootItem,
    RootState,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
)
import newrelic.agent
from newutils import (
    datetime as datetime_utils,
    validations as validation_utils,
)
from notifications import (
    domain as notifications_domain,
)
from organizations import (
    domain as orgs_domain,
)
import re
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
from typing import (
    Any,
    List,
    Optional,
    Tuple,
)
from urllib3.exceptions import (
    LocationParseError,
)
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    unquote,
    urlparse,
)
from uuid import (
    uuid4,
)


def format_root(root: RootItem) -> Root:
    if isinstance(root, GitRootItem):
        return GitRoot(
            branch=root.state.branch,
            cloning_status=GitRootCloningStatus(
                status=root.cloning.status,
                message=root.cloning.reason,
            ),
            environment=root.state.environment,
            environment_urls=root.state.environment_urls,
            git_environment_urls=root.state.git_environment_urls,
            gitignore=root.state.gitignore,
            group_name=root.group_name,
            id=root.id,
            includes_health_check=root.state.includes_health_check,
            last_cloning_status_update=root.cloning.modified_date,
            nickname=root.state.nickname,
            state=root.state.status,
            url=root.state.url,
        )

    if isinstance(root, IPRootItem):
        return IPRoot(
            address=root.metadata.address,
            id=root.id,
            nickname=root.state.nickname,
            port=root.metadata.port,
            state=root.state.status,
        )

    return URLRoot(
        host=root.metadata.host,
        id=root.id,
        nickname=root.state.nickname,
        path=root.metadata.path,
        port=root.metadata.port,
        protocol=root.metadata.protocol,
        state=root.state.status,
    )


@newrelic.agent.function_trace()
async def get_org_roots(*, context: Any, org_id: str) -> Tuple[RootItem, ...]:
    org_groups = await orgs_domain.get_groups(org_id)
    group_roots_loader = context.group_roots

    return tuple(
        root
        for group_roots in await group_roots_loader.load_many(org_groups)
        for root in group_roots
    )


async def _notify_health_check(
    *, group_name: str, request: bool, root: GitRootItem, user_email: str
) -> None:
    if request:
        await notifications_domain.request_health_check(
            branch=root.state.branch,
            group_name=group_name,
            repo_url=root.state.url,
            requester_email=user_email,
        )
    else:
        await notifications_domain.cancel_health_check(
            branch=root.state.branch,
            group_name=group_name,
            repo_url=root.state.url,
            requester_email=user_email,
        )


def _format_git_repo_url(raw_url: str) -> str:
    is_ssh: bool = raw_url.startswith("ssh://") or bool(
        re.match(r"^\w+@.*", raw_url)
    )
    url = (
        f"ssh://{raw_url}"
        if is_ssh and not raw_url.startswith("ssh://")
        else raw_url
    )

    return unquote(url).rstrip(" /")


async def add_git_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group
    group_name: str = kwargs["group_name"].lower()
    url: str = _format_git_repo_url(kwargs["url"])
    branch: str = kwargs["branch"].rstrip()
    nickname: str = _format_root_nickname(kwargs.get("nickname", ""), url)

    gitignore = kwargs["gitignore"]
    enforcer = await authz.get_group_level_enforcer(user_email)

    validations.validate_nickname(nickname)
    group_roots_loader = context.group_roots
    validations.validate_nickname_is_unique(
        nickname, await group_roots_loader.load(group_name)
    )

    if gitignore and not enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()

    if not (
        validations.is_valid_repo_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()

    group = await group_loader.load(group_name)
    if not validations.is_git_unique(
        url,
        branch,
        await get_org_roots(context=context, org_id=group["organization"]),
    ):
        raise RepeatedRoot()

    root = GitRootItem(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason="root created",
            status="UNKNOWN",
        ),
        group_name=group_name,
        id=str(uuid4()),
        metadata=GitRootMetadata(type="Git"),
        state=GitRootState(
            branch=branch,
            environment_urls=list(),
            environment=kwargs["environment"],
            git_environment_urls=list(),
            gitignore=gitignore,
            includes_health_check=kwargs["includes_health_check"],
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            reason=None,
            status="ACTIVE",
            url=url,
        ),
    )
    await roots_model.add(root=root)

    if kwargs["includes_health_check"]:
        await _notify_health_check(
            group_name=group_name,
            request=True,
            root=root,
            user_email=user_email,
        )


async def add_ip_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_loader = context.group
    group_name: str = kwargs["group_name"].lower()
    address: str = kwargs["address"]
    port = str(kwargs["port"])
    is_valid: bool = (
        validations.is_valid_ip(address) and 0 <= int(port) <= 65535
    )

    if not is_valid:
        raise InvalidParameter()

    group = await group_loader.load(group_name)

    if not validations.is_ip_unique(
        address,
        port,
        await get_org_roots(context=context, org_id=group["organization"]),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    validations.validate_nickname(nickname)
    group_roots_loader = context.group_roots
    validations.validate_nickname_is_unique(
        nickname, await group_roots_loader.load(group_name)
    )

    root = IPRootItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=IPRootMetadata(address=address, port=port, type="IP"),
        state=IPRootState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            reason=None,
            status="ACTIVE",
        ),
    )
    await roots_model.add(root=root)


async def add_url_root(context: Any, user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs["group_name"].lower()

    try:
        url_attributes = parse_url(kwargs["url"])
    except LocationParseError:
        raise InvalidParameter()

    if not url_attributes.host or url_attributes.scheme not in {
        "http",
        "https",
    }:
        raise InvalidParameter()

    host: str = url_attributes.host
    path: str = url_attributes.path or "/"
    default_port = "443" if url_attributes.scheme == "https" else "80"
    port = url_attributes.port if url_attributes.port else default_port
    protocol: str = url_attributes.scheme.upper()
    group = await context.group.load(group_name)

    if not validations.is_url_unique(
        host,
        path,
        port,
        protocol,
        await get_org_roots(context=context, org_id=group["organization"]),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    validations.validate_nickname(nickname)
    group_roots_loader = context.group_roots
    validations.validate_nickname_is_unique(
        nickname, await group_roots_loader.load(group_name)
    )

    root = URLRootItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=URLRootMetadata(
            host=host, path=path, port=port, protocol=protocol, type="URL"
        ),
        state=URLRootState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            reason=None,
            status="ACTIVE",
        ),
    )
    await roots_model.add(root=root)


def _get_nickname_from_url(url: str) -> str:
    last_path = urlparse(url).path.split("/")[-1]

    return re.sub(r"(?![a-zA-Z_0-9-]).", "_", last_path[:128])


def _format_root_nickname(nickname: str, url: str) -> str:
    nick = nickname if nickname else _get_nickname_from_url(url)
    # Return the repo name as nickname
    if nick.endswith(".git"):
        return nick[:-4]
    return nick


async def update_git_environments(
    context: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: List[str],
) -> None:
    root_loader: DataLoader = context.root
    root = await root_loader.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    is_valid: bool = root.state.status == "ACTIVE" and all(
        validations.is_valid_url(url) for url in environment_urls
    )
    if not is_valid:
        raise InvalidParameter()

    await roots_model.update_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            branch=root.state.branch,
            environment_urls=environment_urls,
            environment=root.state.environment,
            git_environment_urls=[
                GitEnvironmentUrl(url=item) for item in environment_urls
            ],
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=root.state.nickname,
            other=None,
            reason=None,
            status=root.state.status,
            url=root.state.url,
        ),
    )


async def update_git_root(
    context: Any, user_email: str, **kwargs: Any
) -> None:
    root_id: str = kwargs["id"]
    group_name: str = kwargs["group_name"]
    root_loader: DataLoader = context.root
    root = await root_loader.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    gitignore = kwargs["gitignore"]
    filter_changed: bool = gitignore != root.state.gitignore
    enforcer = await authz.get_group_level_enforcer(user_email)
    if filter_changed and not enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, root.state.url):
        raise InvalidRootExclusion()

    if root.state.status != "ACTIVE":
        raise InvalidParameter()

    nickname = _format_root_nickname(
        kwargs.get("nickname", ""), root.state.url
    )

    validations.validate_nickname(nickname)
    group_roots_loader = context.group_roots
    validations.validate_nickname_is_unique(
        nickname,
        await group_roots_loader.load(group_name),
        old_nickname=root.state.nickname,
    )

    await roots_model.update_root_state(
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            branch=root.state.branch,
            environment=kwargs["environment"],
            environment_urls=root.state.environment_urls,
            git_environment_urls=[
                GitEnvironmentUrl(url=item)
                for item in root.state.environment_urls
            ],
            gitignore=gitignore,
            includes_health_check=kwargs["includes_health_check"],
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            reason=None,
            status=root.state.status,
            url=root.state.url,
        ),
    )

    health_check_changed: bool = (
        kwargs["includes_health_check"] != root.state.includes_health_check
    )
    if health_check_changed:
        await _notify_health_check(
            group_name=group_name,
            request=kwargs["includes_health_check"],
            root=root,
            user_email=user_email,
        )


async def update_root_cloning_status(
    context: Any,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> None:
    validation_utils.validate_field_length(message, 400)
    root_loader: DataLoader = context.root
    root = await root_loader.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    await roots_model.update_git_root_cloning(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason=message,
            status=status,
        ),
        group_name=group_name,
        root_id=root_id,
    )


async def has_open_vulns(
    root: GitRootItem, context: Any, group_name: str
) -> bool:
    return await roots_dal.has_open_vulns(
        nickname=root.state.nickname, context=context, group_name=group_name
    )


async def activate_root(
    *, context: Any, group_name: str, root: RootItem, user_email: str
) -> None:
    new_status = "ACTIVE"

    if root.state.status != new_status:
        group_loader: DataLoader = context.group
        group = await group_loader.load(group_name)
        org_roots = await get_org_roots(
            context=context, org_id=group["organization"]
        )

        if isinstance(root, GitRootItem):
            if not validations.is_git_unique(
                root.state.url, root.state.branch, org_roots
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=GitRootState(
                    branch=root.state.branch,
                    environment_urls=root.state.environment_urls,
                    environment=root.state.environment,
                    git_environment_urls=[
                        GitEnvironmentUrl(url=item)
                        for item in root.state.environment_urls
                    ],
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=None,
                    reason=None,
                    status=new_status,
                    url=root.state.url,
                ),
            )

            if root.state.includes_health_check:
                await notifications_domain.request_health_check(
                    branch=root.state.branch,
                    group_name=group_name,
                    repo_url=root.state.url,
                    requester_email=user_email,
                )

        elif isinstance(root, IPRootItem):
            if not validations.is_ip_unique(
                root.metadata.address, root.metadata.port, org_roots
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=None,
                    reason=None,
                    status=new_status,
                ),
            )

        else:
            if not validations.is_url_unique(
                root.metadata.host,
                root.metadata.path,
                root.metadata.port,
                root.metadata.protocol,
                org_roots,
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=URLRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=None,
                    reason=None,
                    status=new_status,
                ),
            )


async def deactivate_root(
    *,
    group_name: str,
    other: Optional[str],
    reason: str,
    root: RootItem,
    user_email: str,
) -> None:
    new_status = "INACTIVE"

    if root.state.status != new_status:
        if isinstance(root, GitRootItem):
            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=GitRootState(
                    branch=root.state.branch,
                    environment=root.state.environment,
                    environment_urls=root.state.environment_urls,
                    git_environment_urls=[
                        GitEnvironmentUrl(url=item)
                        for item in root.state.environment_urls
                    ],
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=other,
                    reason=reason,
                    status=new_status,
                    url=root.state.url,
                ),
            )

            if root.state.includes_health_check:
                await notifications_domain.cancel_health_check(
                    branch=root.state.branch,
                    group_name=group_name,
                    repo_url=root.state.url,
                    requester_email=user_email,
                )

        elif isinstance(root, IPRootItem):
            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=other,
                    reason=reason,
                    status=new_status,
                ),
            )

        else:
            await roots_model.update_root_state(
                group_name=group_name,
                root_id=root.id,
                state=URLRootState(
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=other,
                    reason=reason,
                    status=new_status,
                ),
            )


async def update_root_state(
    context: Any, user_email: str, group_name: str, root_id: str, state: str
) -> None:
    root_loader: DataLoader = context.root
    root = await root_loader.load((group_name, root_id))
    if state == "ACTIVE":
        await activate_root(
            context=context,
            group_name=group_name,
            root=root,
            user_email=user_email,
        )
    else:
        await deactivate_root(
            group_name=group_name,
            other=None,
            reason="UNKNOWN",
            root=root,
            user_email=user_email,
        )


def get_root_id_by_filename(
    filename: str, group_roots: Tuple[Root, ...]
) -> str:
    root_nickname = filename.split("/")[0]
    file_name_root_ids = [
        root.id
        for root in group_roots
        if isinstance(root, GitRootItem)
        and root.state.nickname == root_nickname
    ]

    if not file_name_root_ids:
        raise RootNotFound()

    return file_name_root_ids[0]


@newrelic.agent.function_trace()
async def get_last_status_update(
    context: Any, root_id: str, current_status: str
) -> str:
    root_states_loader = context.root_states
    historic_state: Tuple[RootState, ...] = await root_states_loader.load(
        root_id
    )

    return next(
        (
            state.modified_date
            for state in reversed(historic_state)
            if state.status != current_status
        ),
        historic_state[0].modified_date,
    )
