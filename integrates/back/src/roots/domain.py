import authz
import boto3
from custom_exceptions import (
    HasVulns,
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RootNotFound,
)
from custom_types import (
    Group,
)
from datetime import (
    datetime,
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
    RootMachineExecutionItem,
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
import pytz  # type: ignore
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
from settings.various import (
    TIME_ZONE,
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
    ParseResult,
    unquote,
    urlparse,
)
from uuid import (
    uuid4,
)


@newrelic.agent.function_trace()
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
            address=root.state.address,
            group_name=root.group_name,
            id=root.id,
            nickname=root.state.nickname,
            port=root.state.port,
            state=root.state.status,
        )

    return URLRoot(
        group_name=root.group_name,
        host=root.state.host,
        id=root.id,
        nickname=root.state.nickname,
        path=root.state.path,
        port=root.state.port,
        protocol=root.state.protocol,
        state=root.state.status,
    )


@newrelic.agent.function_trace()
async def get_org_roots(*, loaders: Any, org_id: str) -> Tuple[RootItem, ...]:
    org_groups = await orgs_domain.get_groups(org_id)

    return tuple(
        root
        for group_roots in await loaders.group_roots.load_many(org_groups)
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


async def add_git_root(
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name: str = kwargs["group_name"].lower()
    url: str = _format_git_repo_url(kwargs["url"])
    branch: str = kwargs["branch"].rstrip()
    nickname: str = _format_root_nickname(kwargs.get("nickname", ""), url)

    loaders.group_roots.clear(group_name)
    if not (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    gitignore = kwargs["gitignore"]
    enforcer = await authz.get_group_level_enforcer(user_email)
    if gitignore and not enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()

    group = await loaders.group.load(group_name)
    if ensure_org_uniqueness and not validations.is_git_unique(
        url,
        await get_org_roots(loaders=loaders, org_id=group["organization"]),
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
        machine_execution=[],
        metadata=GitRootMetadata(type="Git"),
        state=GitRootState(
            branch=branch,
            environment_urls=[],
            environment=kwargs["environment"],
            git_environment_urls=[],
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

    return root.id


async def add_ip_root(
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name: str = kwargs["group_name"].lower()
    address: str = kwargs["address"]
    port = str(kwargs["port"])
    is_valid: bool = (
        validations.is_valid_ip(address) and 0 <= int(port) <= 65535
    )

    if not is_valid:
        raise InvalidParameter()

    group = await loaders.group.load(group_name)

    if ensure_org_uniqueness and not validations.is_ip_unique(
        address,
        port,
        await get_org_roots(loaders=loaders, org_id=group["organization"]),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    loaders.group_roots.clear(group_name)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    root = IPRootItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=IPRootMetadata(type="IP"),
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            port=port,
            reason=None,
            status="ACTIVE",
        ),
    )
    await roots_model.add(root=root)

    return root.id


async def add_url_root(
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name: str = kwargs["group_name"].lower()

    try:
        url_attributes = parse_url(kwargs["url"])
    except LocationParseError as ex:
        raise InvalidParameter() from ex

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
    group = await loaders.group.load(group_name)

    if ensure_org_uniqueness and not validations.is_url_unique(
        host,
        path,
        port,
        protocol,
        await get_org_roots(loaders=loaders, org_id=group["organization"]),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    loaders.group_roots.clear(group_name)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    root = URLRootItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=URLRootMetadata(type="URL"),
        state=URLRootState(
            host=host,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            nickname=nickname,
            other=None,
            path=path,
            port=port,
            protocol=protocol,
            reason=None,
            status="ACTIVE",
        ),
    )
    await roots_model.add(root=root)

    return root.id


def _get_nickname_from_url(url: str) -> str:
    url_attributes: ParseResult = urlparse(url)
    if not url_attributes.path:
        last_path: str = urlparse(url).netloc.split(":")[-1]
    else:
        last_path = urlparse(url).path.split("/")[-1]

    return re.sub(r"(?![a-zA-Z_0-9-]).", "_", last_path[:128])


def _format_root_nickname(nickname: str, url: str) -> str:
    nick: str = nickname if nickname else _get_nickname_from_url(url)
    # Return the repo name as nickname
    if nick.endswith("_git"):
        return nick[:-4]
    return nick


async def update_git_environments(
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: List[str],
) -> None:
    root: RootItem = await loaders.root.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    is_valid: bool = root.state.status == "ACTIVE" and all(
        validations.is_valid_url(url) for url in environment_urls
    )
    if not is_valid:
        raise InvalidParameter()

    await roots_model.update_root_state(
        current_value=root.state,
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
    loaders: Any, user_email: str, **kwargs: Any
) -> None:
    root_id: str = kwargs["id"]
    group_name: str = kwargs["group_name"]
    root: RootItem = await loaders.root.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    if root.state.status != "ACTIVE":
        raise InvalidParameter()

    url: str = kwargs["url"]
    branch: str = kwargs["branch"]
    if not (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()

    if url != root.state.url:
        if await roots_dal.get_root_vulns(
            nickname=root.state.nickname,
            loaders=loaders,
            group_name=group_name,
        ):
            raise HasVulns()
        group = await loaders.group.load(group_name)
        if not validations.is_git_unique(
            url,
            await get_org_roots(loaders=loaders, org_id=group["organization"]),
        ):
            raise RepeatedRoot()

    gitignore = kwargs["gitignore"]
    enforcer = await authz.get_group_level_enforcer(user_email)
    if gitignore != root.state.gitignore and not enforcer(
        group_name, "update_git_root_filter"
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, root.state.url):
        raise InvalidRootExclusion()

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            branch=branch,
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
            nickname=root.state.nickname,
            other=None,
            reason=None,
            status=root.state.status,
            url=url,
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
    loaders: Any,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
) -> None:
    validation_utils.validate_field_length(message, 400)
    root: RootItem = await loaders.root.load((group_name, root_id))

    if not isinstance(root, GitRootItem):
        raise InvalidParameter()

    await roots_model.update_git_root_cloning(
        current_value=root.cloning,
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason=message,
            status=status,
        ),
        group_name=group_name,
        root_id=root_id,
    )


async def activate_root(
    *, loaders: Any, group_name: str, root: RootItem, user_email: str
) -> None:
    new_status = "ACTIVE"

    if root.state.status != new_status:
        group = await loaders.group.load(group_name)
        org_roots = await get_org_roots(
            loaders=loaders, org_id=group["organization"]
        )

        if isinstance(root, GitRootItem):
            if not validations.is_git_unique(root.state.url, org_roots):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                current_value=root.state,
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
                root.state.address, root.state.port, org_roots
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    address=root.state.address,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=None,
                    port=root.state.port,
                    reason=None,
                    status=new_status,
                ),
            )

        else:
            if not validations.is_url_unique(
                root.state.host,
                root.state.path,
                root.state.port,
                root.state.protocol,
                org_roots,
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=URLRootState(
                    host=root.state.host,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=None,
                    path=root.state.path,
                    port=root.state.port,
                    protocol=root.state.protocol,
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
                current_value=root.state,
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
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    address=root.state.address,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=other,
                    port=root.state.port,
                    reason=reason,
                    status=new_status,
                ),
            )

        else:
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=URLRootState(
                    host=root.state.host,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    nickname=root.state.nickname,
                    other=other,
                    path=root.state.path,
                    port=root.state.port,
                    protocol=root.state.protocol,
                    reason=reason,
                    status=new_status,
                ),
            )


async def update_root_state(
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    state: str,
) -> None:
    root: RootItem = await loaders.root.load((group_name, root_id))
    if state == "ACTIVE":
        await activate_root(
            loaders=loaders,
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


def get_root_id_by_nickname(
    nickname: str, group_roots: Tuple[RootItem, ...]
) -> str:
    # There are roots with the same nickname
    # then It is going to take the last modified root
    sorted_roots = sorted(
        group_roots,
        key=lambda root: datetime.fromisoformat(root.state.modified_date),
        reverse=True,
    )
    for root in sorted_roots:
        if isinstance(root, GitRootItem) and root.state.nickname == nickname:
            return root.id

    raise RootNotFound()


@newrelic.agent.function_trace()
async def get_last_status_update(
    loaders: Any, root_id: str, current_status: str
) -> str:
    historic_state: Tuple[RootState, ...] = await loaders.root_states.load(
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


def _format_input_url(url: str) -> str:
    return (
        url.strip()
        .replace("https://", "")
        .replace("http://", "")
        .replace("www.", "")
        .split("/")[0]
    )


def get_unreliable_root_id_by_component(
    component: str, group_roots: Tuple[RootItem, ...], group: Group
) -> str:
    if not component:
        return ""

    formatted_component = _format_input_url(component)
    has_black_service = group["service"] == "BLACK"
    has_white_service = group["service"] == "WHITE"
    return next(
        (
            root.id
            for root in group_roots
            if (
                has_white_service
                and isinstance(root, GitRootItem)
                and (
                    formatted_component
                    in set(map(_format_input_url, root.state.environment_urls))
                )
            )
            or (
                has_black_service
                and isinstance(root, URLRootItem)
                and _format_input_url(root.state.host) == formatted_component
            )
        ),
        "",
    )


async def move_root(
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    target_group_name: str,
) -> str:
    root: RootItem = await loaders.root.load((group_name, root_id))
    source_group, target_group = await loaders.group.load_many(
        [group_name, target_group_name]
    )

    if (
        root.state.status != "ACTIVE"
        or target_group_name == root.group_name
        or target_group_name
        not in await orgs_domain.get_groups(source_group["organization"])
        or source_group["service"] != target_group["service"]
    ):
        raise InvalidParameter()

    target_group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        target_group_name
    )

    if isinstance(root, GitRootItem):
        if not validations.is_git_unique(root.state.url, target_group_roots):
            raise RepeatedRoot()

        new_root_id = await add_git_root(
            loaders,
            user_email,
            ensure_org_uniqueness=False,
            branch=root.state.branch,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            group_name=target_group_name,
            includes_health_check=root.state.includes_health_check,
            nickname=root.state.nickname,
            url=root.state.url,
        )
    elif isinstance(root, IPRootItem):
        if not validations.is_ip_unique(
            root.state.url, root.state.branch, target_group_roots
        ):
            raise RepeatedRoot()

        new_root_id = await add_ip_root(
            loaders,
            user_email,
            ensure_org_uniqueness=False,
            address=root.state.address,
            group_name=target_group_name,
            nickname=root.state.nickname,
            port=root.state.port,
        )
    else:
        if not validations.is_url_unique(
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol,
            target_group_roots,
        ):
            raise RepeatedRoot()

        new_root_id = await add_url_root(
            loaders,
            user_email,
            ensure_org_uniqueness=False,
            group_name=target_group_name,
            nickname=root.state.nickname,
            url=(
                f"{root.state.protocol}://{root.state.host}:{root.state.port}"
                f"{root.state.path}"
            ),
        )

    await deactivate_root(
        group_name=group_name,
        other=target_group_name,
        reason="MOVED_TO_ANOTHER_GROUP",
        root=root,
        user_email=user_email,
    )

    return new_root_id


async def add_machine_execution(
    root_id: str,
    job_id: str,
    **kwargs: Any,
) -> bool:
    client = boto3.client("batch")
    tzn = pytz.timezone(TIME_ZONE)

    response = client.describe_jobs(jobs=[job_id])
    jobs = response.get("jobs", [])

    start_date = kwargs.pop("started_at").astimezone(tzn)

    try:
        current_job = jobs[0]
    except IndexError:
        return False

    queue_date = datetime.fromtimestamp(
        int(current_job["createdAt"] / 1000)
    ).astimezone(tzn)
    end_date = kwargs.pop("stopped_at").astimezone(tzn)
    execution = RootMachineExecutionItem(
        job_id=job_id,
        name=current_job["jobName"],
        queue=current_job["jobQueue"].split("/")[-1],
        created_at=datetime_utils.get_as_str(queue_date),
        started_at=datetime_utils.get_as_str(start_date),
        stopped_at=datetime_utils.get_as_str(end_date),
        findings_executed=kwargs.pop("findings_executed", []),
    )
    return await roots_model.add_machine_execution(root_id, execution)
