# pylint: disable=too-many-lines

import authz
import base64
import binascii
import boto3
from custom_exceptions import (
    HasVulns,
    InvalidParameter,
    InvalidRootExclusion,
    PermissionDenied,
    RepeatedRoot,
    RootNotFound,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as creds_model,
    roots as roots_model,
)
from db_model.credentials.types import (
    CredentialItem,
    CredentialMetadata,
    CredentialState,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootState,
    IPRootItem,
    IPRootState,
    RootItem,
    RootMachineExecutionItem,
    RootState,
    RootUnreliableIndicators,
    Secret,
    URLRootItem,
    URLRootState,
)
from itertools import (
    groupby,
)
from newutils import (
    datetime as datetime_utils,
    validations as validation_utils,
)
from notifications import (
    domain as notifications_domain,
)
from operator import (
    attrgetter,
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
    GitEnvironmentUrl as GitEnvironmentUrlOld,
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
    Dict,
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


def format_root(root: RootItem) -> Root:
    if isinstance(root, GitRootItem):
        return GitRoot(
            branch=root.state.branch,
            cloning_status=GitRootCloningStatus(
                status=root.cloning.status.value,
                message=root.cloning.reason,
                commit=root.cloning.commit,
            ),
            environment=root.state.environment,
            environment_urls=root.state.environment_urls,
            git_environment_urls=[
                GitEnvironmentUrlOld(url=env.url)
                for env in root.state.git_environment_urls
            ],
            gitignore=root.state.gitignore,
            group_name=root.group_name,
            id=root.id,
            includes_health_check=root.state.includes_health_check,
            last_cloning_status_update=root.cloning.modified_date,
            last_state_status_update=(
                root.unreliable_indicators.unreliable_last_status_update
            ),
            nickname=root.state.nickname,
            state=root.state.status,
            url=root.state.url,
            use_vpn=root.state.use_vpn,
        )

    if isinstance(root, IPRootItem):
        return IPRoot(
            address=root.state.address,
            group_name=root.group_name,
            id=root.id,
            nickname=root.state.nickname,
            port=int(root.state.port),
            state=root.state.status,
        )

    return URLRoot(
        group_name=root.group_name,
        host=root.state.host,
        id=root.id,
        nickname=root.state.nickname,
        path=root.state.path,
        port=int(root.state.port),
        protocol=root.state.protocol,
        state=root.state.status,
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


async def add_git_root(  # pylint: disable=too-many-locals
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> GitRootItem:
    group_name = str(kwargs["group_name"]).lower()
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

    includes_health_check = kwargs["includes_health_check"]
    service_enforcer = await authz.get_group_service_attributes_enforcer(
        group_name
    )
    if includes_health_check and not service_enforcer("has_squad"):
        raise PermissionDenied()

    gitignore = kwargs["gitignore"]
    group_enforcer = await authz.get_group_level_enforcer(user_email)
    if gitignore and not group_enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()

    group: Group = await loaders.group_typed.load(group_name)
    if ensure_org_uniqueness and not validations.is_git_unique(
        url,
        branch,
        await loaders.organization_roots.load(group.organization_name),
    ):
        raise RepeatedRoot()

    modified_date = datetime_utils.get_iso_date()
    root = GitRootItem(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason="root created",
            status=GitCloningStatus("UNKNOWN"),
        ),
        group_name=group_name,
        id=str(uuid4()),
        organization_name=group.organization_name,
        state=GitRootState(
            branch=branch,
            environment_urls=[],
            environment=kwargs["environment"],
            git_environment_urls=[],
            gitignore=gitignore,
            includes_health_check=includes_health_check,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            reason=None,
            status="ACTIVE",
            url=url,
            use_vpn=kwargs.get("use_vpn", False),
        ),
        type="Git",
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
    )

    credentials = kwargs.get("credentials")
    if credentials:
        credential = _format_root_credential(
            credentials, group_name, user_email, root.id
        )
        await creds_model.add(credential=credential)

    await roots_model.add(root=root)

    if includes_health_check:
        await _notify_health_check(
            group_name=group_name,
            request=True,
            root=root,
            user_email=user_email,
        )

    return root


async def add_ip_root(
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    address: str = kwargs["address"]
    port = str(kwargs["port"])
    is_valid: bool = (
        validations.is_valid_ip(address) and 0 <= int(port) <= 65535
    )

    if not is_valid:
        raise InvalidParameter()

    group: Group = await loaders.group_typed.load(group_name)
    if ensure_org_uniqueness and not validations.is_ip_unique(
        address,
        port,
        await loaders.organization_roots.load(group.organization_name),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    loaders.group_roots.clear(group_name)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    modified_date = datetime_utils.get_iso_date()
    root = IPRootItem(
        group_name=group_name,
        id=str(uuid4()),
        organization_name=group.organization_name,
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            port=port,
            reason=None,
            status="ACTIVE",
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type="IP",
    )
    await roots_model.add(root=root)

    return root.id


async def add_url_root(
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()

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

    group: Group = await loaders.group_typed.load(group_name)
    if ensure_org_uniqueness and not validations.is_url_unique(
        host,
        path,
        port,
        protocol,
        await loaders.organization_roots.load(group.organization_name),
    ):
        raise RepeatedRoot()

    loaders.group_roots.clear(group_name)
    validations.validate_nickname(kwargs["nickname"])
    validations.validate_nickname_is_unique(
        kwargs["nickname"], await loaders.group_roots.load(group_name)
    )

    modified_date = datetime_utils.get_iso_date()
    root = URLRootItem(
        group_name=group_name,
        id=str(uuid4()),
        organization_name=group.organization_name,
        state=URLRootState(
            host=host,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=kwargs["nickname"],
            other=None,
            path=path,
            port=port,
            protocol=protocol,
            reason=None,
            status="ACTIVE",
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type="URL",
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


def _format_credential_key(key_type: CredentialType, key: str) -> str:
    encoded_key = key
    if key_type.value == "SSH":
        try:
            raw_key: str = base64.b64decode(key).decode()
        except binascii.Error as exc:
            raise InvalidParameter() from exc

        if not raw_key.endswith("\n"):
            raw_key += "\n"
        encoded_key = base64.b64encode(raw_key.encode()).decode()

    return encoded_key


def _format_root_credential(
    credentials: Dict[str, str], group_name: str, user_email: str, root_id: str
) -> CredentialItem:
    credential_name = credentials["name"]
    credential_type = CredentialType(credentials["type"])

    if not credential_name:
        raise InvalidParameter()

    return CredentialItem(
        group_name=group_name,
        id=str(uuid4()),
        metadata=CredentialMetadata(type=credential_type),
        state=CredentialState(
            key=_format_credential_key(credential_type, credentials["key"])
            if "key" in credentials
            else None,
            user=credentials.get("user"),
            password=credentials.get("password"),
            token=credentials.get("token"),
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            name=credential_name,
            roots=[root_id],
        ),
    )


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
            use_vpn=root.state.use_vpn,
        ),
    )


async def update_root_credentials(
    loaders: Any,
    credentials: Dict[str, str],
    group_name: str,
    user_email: str,
    root_id: str,
) -> None:
    existing_credential: Optional[CredentialItem] = None
    credential_id: Optional[str] = credentials.get("id")
    if credential_id:
        existing_credential = await loaders.credential.load(
            (group_name, credential_id)
        )
    if (
        credentials.get("key")
        or credentials.get("token")
        or (credentials.get("user") and credentials.get("password"))
    ):
        credential = _format_root_credential(
            credentials, group_name, user_email, root_id
        )
        await creds_model.add(credential=credential)
        if existing_credential:
            await creds_model.remove(
                credential_id=existing_credential.id,
                group_name=existing_credential.group_name,
            )
    elif existing_credential:
        new_credential_name = credentials["name"]
        if (
            new_credential_name
            and new_credential_name != existing_credential.state.name
        ):
            await creds_model.update_credential_state(
                current_value=existing_credential.state,
                group_name=group_name,
                credential_id=existing_credential.id,
                state=CredentialState(
                    key=existing_credential.state.key,
                    user=existing_credential.state.user,
                    password=existing_credential.state.password,
                    token=existing_credential.state.token,
                    modified_by=user_email,
                    modified_date=datetime_utils.get_iso_date(),
                    name=new_credential_name,
                    roots=existing_credential.state.roots,
                ),
            )


async def update_git_root(
    loaders: Any, user_email: str, **kwargs: Any
) -> RootItem:
    root_id: str = kwargs["id"]
    group_name = str(kwargs["group_name"]).lower()
    root: RootItem = await loaders.root.load((group_name, root_id))

    url: str = kwargs["url"]
    branch: str = kwargs["branch"]
    if not (
        isinstance(root, GitRootItem)
        and root.state.status == "ACTIVE"
        and validations.is_valid_url(url)
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
        group: Group = await loaders.group_typed.load(group_name)
        if not validations.is_git_unique(
            url,
            branch,
            await loaders.organization_roots.load(group.organization_name),
        ):
            raise RepeatedRoot()

    health_check_changed: bool = (
        kwargs["includes_health_check"] != root.state.includes_health_check
    )
    if health_check_changed:
        service_enforcer = await authz.get_group_service_attributes_enforcer(
            group_name
        )
        if kwargs["includes_health_check"] and not service_enforcer(
            "has_squad"
        ):
            raise PermissionDenied()
        await _notify_health_check(
            group_name=group_name,
            request=kwargs["includes_health_check"],
            root=root,
            user_email=user_email,
        )

    gitignore = kwargs["gitignore"]
    enforcer = await authz.get_group_level_enforcer(user_email)
    if gitignore != root.state.gitignore and not enforcer(
        group_name, "update_git_root_filter"
    ):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, root.state.url):
        raise InvalidRootExclusion()

    credentials = kwargs.get("credentials")
    if credentials:
        await update_root_credentials(
            loaders, credentials, group_name, user_email, root_id
        )

    new_state = GitRootState(
        branch=branch,
        environment=kwargs["environment"],
        environment_urls=root.state.environment_urls,
        git_environment_urls=[
            GitEnvironmentUrl(url=item) for item in root.state.environment_urls
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
        use_vpn=kwargs.get("use_vpn", None)
        if kwargs.get("use_vpn") is not None
        else root.state.use_vpn,
    )
    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    return GitRootItem(
        cloning=root.cloning,
        group_name=root.group_name,
        id=root.id,
        organization_name=root.organization_name,
        state=new_state,
        type=root.type,
        unreliable_indicators=root.unreliable_indicators,
    )


async def update_root_cloning_status(  # pylint: disable=too-many-arguments
    loaders: Any,
    group_name: str,
    root_id: str,
    status: str,
    message: str,
    commit: Optional[str] = None,
    commit_date: Optional[str] = None,
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
            status=GitCloningStatus(status),
            commit=commit,
            commit_date=commit_date,
        ),
        group_name=group_name,
        root_id=root_id,
    )


async def activate_root(
    *, loaders: Any, group_name: str, root: RootItem, user_email: str
) -> None:
    new_status = "ACTIVE"

    if root.state.status != new_status:
        group: Group = await loaders.group_typed.load(group_name)
        org_roots = await loaders.organization_roots.load(
            group.organization_name
        )

        if isinstance(root, GitRootItem):
            if not validations.is_git_unique(
                root.state.url, root.state.branch, org_roots
            ):
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
                    use_vpn=root.state.use_vpn,
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
                    use_vpn=root.state.use_vpn,
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
    nickname: str,
    group_roots: Tuple[RootItem, ...],
    only_git_roots: bool = False,
) -> str:
    root_ids_by_nicknames = get_root_ids_by_nicknames(
        group_roots=group_roots, only_git_roots=only_git_roots
    )
    return get_root_id_by_nicknames(
        nickname=nickname, root_ids_by_nicknames=root_ids_by_nicknames
    )


def get_root_id_by_nicknames(
    nickname: str,
    root_ids_by_nicknames: Dict[str, str],
) -> str:
    try:
        root_id = root_ids_by_nicknames[nickname]
    except KeyError as exc:
        raise RootNotFound() from exc

    return root_id


def get_root_ids_by_nicknames(
    group_roots: Tuple[RootItem, ...], only_git_roots: bool = False
) -> Dict[str, str]:
    # Get a dict that have the relation between nickname and id for roots
    # There are roots with the same nickname
    # then It is going to take the last modified root
    sorted_roots = sorted(
        group_roots,
        key=lambda root: datetime.fromisoformat(root.state.modified_date),
        reverse=False,
    )
    root_ids: Dict[str, str] = {}
    for root in sorted_roots:
        if not only_git_roots or isinstance(root, GitRootItem):
            root_ids[root.state.nickname] = root.id

    return root_ids


async def get_last_status_update(loaders: Any, root_id: str) -> RootState:
    """
    Returns the state item where the status last changed

    ACTIVE, [ACTIVE], INACTIVE, ACTIVE
    """
    historic_state: Tuple[RootState, ...] = await loaders.root_states.load(
        root_id
    )
    status_changes = tuple(
        tuple(group)
        for _, group in groupby(historic_state, key=attrgetter("status"))
    )
    with_current_status = status_changes[-1]

    return with_current_status[0]


async def get_last_status_update_date(loaders: Any, root_id: str) -> str:
    """Returns the date where the status last changed"""
    last_status_update = await get_last_status_update(loaders, root_id)

    return last_status_update.modified_date


async def move_root(
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    target_group_name: str,
) -> str:
    root: RootItem = await loaders.root.load((group_name, root_id))
    source_group: Group = await loaders.group_typed.load(group_name)
    source_org_id = await orgs_domain.get_id_for_group(group_name)
    target_group: Group = await loaders.group_typed.load(target_group_name)

    if (
        root.state.status != "ACTIVE"
        or target_group_name == root.group_name
        or target_group_name not in await orgs_domain.get_groups(source_org_id)
        or source_group.state.service != target_group.state.service
    ):
        raise InvalidParameter()

    target_group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        target_group_name
    )

    if isinstance(root, GitRootItem):
        if not validations.is_git_unique(
            root.state.url, root.state.branch, target_group_roots
        ):
            raise RepeatedRoot()

        new_root = await add_git_root(
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
        new_root_id = new_root.id
    elif isinstance(root, IPRootItem):
        if not validations.is_ip_unique(
            root.state.address, root.state.port, target_group_roots
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

    start_date = (
        kwargs.pop("started_at").astimezone(tzn)
        if "started_at" in kwargs
        else None
    )

    try:
        current_job = jobs[0]
    except IndexError:
        return False

    queue_date = datetime.fromtimestamp(
        int(current_job["createdAt"] / 1000)
    ).astimezone(tzn)

    execution = RootMachineExecutionItem(
        root_id=root_id,
        job_id=job_id,
        name=current_job["jobName"],
        queue=current_job["jobQueue"].split("/")[-1],
        created_at=datetime_utils.get_as_str(queue_date),
        started_at=datetime_utils.get_as_str(start_date)
        if start_date
        else None,
        findings_executed=list(kwargs.pop("findings_executed", [])),
        commit=kwargs.pop("git_commit", ""),
    )
    return await roots_model.add_machine_execution(root_id, execution)


async def add_secret(  # pylint: disable=too-many-arguments
    loaders: Any,
    group_name: str,
    root_id: str,
    key: str,
    value: str,
    description: Optional[str] = None,
) -> bool:
    await loaders.root.load((group_name, root_id))
    secret = Secret(key=key, value=value, description=description)
    return await roots_model.add_secret(root_id, secret)


async def remove_secret(root_id: str, secret_key: str) -> None:
    await roots_model.remove_secret(root_id, secret_key)


async def finish_machine_execution(
    root_id: str,
    job_id: str,
    **kwargs: Any,
) -> bool:
    stop_date = kwargs.pop("stopped_at").astimezone(pytz.timezone(TIME_ZONE))

    return await roots_model.finish_machine_execution(
        root_id,
        job_id,
        stopped_at=datetime_utils.get_as_str(stop_date),
        findings_executed=kwargs.pop("findings_executed", []),
        status=kwargs.pop("status", "SUCCESS"),
    )


async def start_machine_execution(
    root_id: str,
    job_id: str,
    **kwargs: Any,
) -> bool:
    started_at = kwargs.pop("started_at").astimezone(pytz.timezone(TIME_ZONE))

    return await roots_model.start_machine_execution(
        root_id,
        job_id,
        started_at=datetime_utils.get_as_str(started_at),
        git_commit=kwargs.pop("git_commit", None),
    )


async def validate_git_access(**kwargs: Any) -> None:
    url: str = _format_git_repo_url(kwargs["url"])
    cred_type: CredentialType = CredentialType(kwargs["credentials"]["type"])
    if key := kwargs["credentials"].get("key"):
        kwargs["credentials"]["key"] = _format_credential_key(cred_type, key)
    await validations.validate_git_credentials(
        url, cred_type, kwargs["credentials"]
    )
