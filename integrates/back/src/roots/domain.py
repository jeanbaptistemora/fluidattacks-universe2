# pylint: disable=too-many-lines

import aioboto3
from aioextensions import (
    collect,
    schedule,
)
import authz
import base64
import binascii
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
)
from custom_exceptions import (
    CredentialNotFound,
    HasVulns,
    InvalidField,
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
from db_model.credentials import (
    update_root_ids,
)
from db_model.credentials.get import (
    get_credentials,
)
from db_model.credentials.types import (
    CredentialItem,
    CredentialMetadata,
    CredentialState,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
    Notification,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitEnvironmentCloud,
    GitEnvironmentUrl,
    GitEnvironmentUrlType,
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    Root,
    RootMachineExecution,
    RootState,
    RootUnreliableIndicators,
    Secret,
    URLRoot,
    URLRootState,
)
from group_access import (
    domain as group_access_domain,
)
import hashlib
from itertools import (
    groupby,
)
from mailer import (
    groups as groups_mail,
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
    validations,
)
from settings.various import (
    TIME_ZONE,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
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


async def _notify_health_check(
    *, group_name: str, request: bool, root: GitRoot, user_email: str
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


def format_git_repo_url(raw_url: str) -> str:
    is_ssh: bool = raw_url.startswith("ssh://") or bool(
        re.match(r"^\w+@.*", raw_url)
    )
    if not is_ssh:
        raw_url = str(parse_url(raw_url)._replace(auth=None))
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
) -> GitRoot:
    group_name = str(kwargs["group_name"]).lower()
    group: Group = await loaders.group.load(group_name)
    url: str = format_git_repo_url(kwargs["url"])
    branch: str = kwargs["branch"].rstrip()
    nickname: str = _format_root_nickname(kwargs.get("nickname", ""), url)

    loaders.group_roots.clear(group_name)
    if not (
        validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()
    validation_utils.validate_sanitized_csv_input(
        nickname, url, kwargs["environment"]
    )
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    includes_health_check = kwargs["includes_health_check"]
    service_enforcer = await authz.get_group_service_attributes_enforcer(group)
    if includes_health_check and not service_enforcer("has_squad"):
        raise PermissionDenied()

    gitignore = kwargs["gitignore"]
    group_enforcer = await authz.get_group_level_enforcer(user_email)
    if gitignore and not group_enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    organization_name = organization.id
    if ensure_org_uniqueness and not validations.is_git_unique(
        url,
        branch,
        await loaders.organization_roots.load(organization_name),
    ):
        raise RepeatedRoot()

    modified_date = datetime_utils.get_iso_date()
    root = GitRoot(
        cloning=GitRootCloning(
            modified_date=datetime_utils.get_iso_date(),
            reason="root created",
            status=GitCloningStatus("UNKNOWN"),
        ),
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
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
            status=RootStatus.ACTIVE,
            url=url,
            use_vpn=kwargs.get("use_vpn", False),
        ),
        type=RootType.GIT,
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
    )

    credentials: Optional[Dict[str, str]] = cast(
        Optional[Dict[str, str]], kwargs.get("credentials")
    )

    if credentials:
        if (credential_id := credentials.get("id")) and credential_id:
            credential: CredentialItem = await loaders.credential.load(
                (group_name, credential_id)
            )
            await update_root_ids(
                current_value=credential.state,
                modified_by=user_email,
                group_name=group_name,
                credential_id=credential.id,
                root_ids=(
                    *credential.state.roots,
                    root.id,
                ),
            )
        else:
            credential = _format_root_credential(
                credentials, group_name, user_email, root.id
            )
            group_credentials: Tuple[
                CredentialItem, ...
            ] = await loaders.group_credentials.load(root.group_name)
            validations.validate_credential_name(credential, group_credentials)
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

    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    organization_name = organization.name
    if ensure_org_uniqueness and not validations.is_ip_unique(
        address,
        port,
        await loaders.organization_roots.load(organization_name),
    ):
        raise RepeatedRoot()

    nickname = kwargs["nickname"]
    loaders.group_roots.clear(group_name)
    validation_utils.validate_sanitized_csv_input(nickname)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    modified_date = datetime_utils.get_iso_date()
    root = IPRoot(
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            port=port,
            reason=None,
            status=RootStatus.ACTIVE,
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type=RootType.IP,
    )
    await roots_model.add(root=root)

    return root.id


async def add_url_root(  # pylint: disable=too-many-locals
    loaders: Any,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    nickname: str = str(kwargs["nickname"])
    url: str = str(kwargs["url"])
    validation_utils.validate_sanitized_csv_input(url, nickname)

    try:
        url_attributes = parse_url(url)
    except LocationParseError as ex:
        raise InvalidParameter() from ex

    if not url_attributes.host or url_attributes.scheme not in {
        "http",
        "https",
    }:
        raise InvalidParameter()

    host: str = url_attributes.host
    path: str = url_attributes.path or "/"
    query: Optional[str] = url_attributes.query
    default_port = "443" if url_attributes.scheme == "https" else "80"
    port = url_attributes.port if url_attributes.port else default_port
    protocol: str = url_attributes.scheme.upper()

    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    organization_name = organization.name
    if ensure_org_uniqueness and not validations.is_url_unique(
        host,
        path,
        port,
        protocol,
        query,
        await loaders.organization_roots.load(organization_name),
    ):
        raise RepeatedRoot()

    loaders.group_roots.clear(group_name)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )

    modified_date = datetime_utils.get_iso_date()
    root = URLRoot(
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
        state=URLRootState(
            host=host,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
            reason=None,
            status=RootStatus.ACTIVE,
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type=RootType.URL,
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
            if "key" in credentials and credentials["key"]
            else None,
            user=credentials.get("user") or None,
            password=credentials.get("password") or None,
            token=credentials.get("token") or None,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            name=credential_name,
            roots=[root_id],
        ),
    )


async def update_git_environments(  # pylint: disable=too-many-arguments
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: List[str],
    reason: Optional[str],
    other: Optional[str],
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    modified_date: str = datetime_utils.get_iso_date()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    is_valid: bool = root.state.status == RootStatus.ACTIVE and all(
        validations.is_valid_url(url) for url in environment_urls
    )
    if not is_valid:
        raise InvalidParameter()

    # pylint: disable=unnecessary-comprehension
    urls_deleted: List[str] = [
        url
        for url in set(root.state.environment_urls).difference(
            set(environment_urls)
        )
    ]
    urls_added: List[str] = [
        url
        for url in environment_urls
        if url not in root.state.environment_urls
    ]

    if urls_deleted:
        if not reason:
            raise InvalidParameter(field="Reason")
        if reason == "OTHER" and not other:
            raise InvalidParameter(field="Other")

    await collect(
        [remove_environment_url(root_id, url) for url in urls_deleted]
    )
    await collect(
        [
            add_git_environment_url(
                loaders, group_name, root_id, url, url_type="URL"
            )
            for url in urls_added
        ]
    )

    if urls_added or urls_deleted:
        await send_mail_environment(
            loaders=loaders,
            date=modified_date,
            group_name=group_name,
            git_root=root.state.nickname,
            urls_added=urls_added,
            urls_deleted=urls_deleted,
            user_email=user_email,
            other=other,
            reason=reason,
        )

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=GitRootState(
            branch=root.state.branch,
            environment_urls=environment_urls,
            environment=root.state.environment,
            git_environment_urls=[],
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=root.state.nickname,
            other=other,
            reason=reason,
            status=root.state.status,
            url=root.state.url,
            use_vpn=root.state.use_vpn,
        ),
    )


async def _remove_root_from_credential(
    root_id: str,
    group_name: str,
    user_email: str,
    credential: Optional[CredentialItem],
) -> None:
    if credential:
        credential_roots = [*credential.state.roots]
        credential_roots.remove(root_id)
        await update_root_ids(
            current_value=credential.state,
            modified_by=user_email,
            group_name=group_name,
            credential_id=credential.id,
            root_ids=tuple(credential_roots),
        )

    # Check the others credential until cleaning up the db
    group_credentials = await get_credentials(group_name=group_name)
    for cred in group_credentials:
        if root_id in cred.state.roots:
            cred_roots = [*cred.state.roots]
            cred_roots.remove(root_id)
            await update_root_ids(
                current_value=cred.state,
                modified_by=user_email,
                group_name=group_name,
                credential_id=cred.id,
                root_ids=tuple(cred_roots),
            )


async def _update_git_root_credentials(  # noqa: MC0001
    loaders: Any,
    root: GitRoot,
    credentials: Optional[Dict[str, str]],
    user_email: str,
) -> None:
    credential_id = credentials.get("id") if credentials else None
    credential_to_add = None
    if credentials and credential_id is None:
        credential_to_add = _format_root_credential(
            credentials, root.group_name, user_email, root.id
        )

    group_credentials: Tuple[
        CredentialItem, ...
    ] = await loaders.group_credentials.load(root.group_name)
    current_credential = next(
        (
            credential
            for credential in group_credentials
            if root.id in credential.state.roots
        ),
        None,
    )
    credential_to_update = next(
        (
            credential
            for credential in group_credentials
            if credential_id == credential.id
        ),
        None,
    )
    if credential_to_update is None and credential_id is not None:
        raise CredentialNotFound()

    if credential_to_update is None and credential_to_add:
        # Add new credential to group and delete credential if only that root
        validations.validate_credential_name(
            credential_to_add, group_credentials
        )

        await _remove_root_from_credential(
            root.id, root.group_name, user_email, current_credential
        )
        await creds_model.add(credential=credential_to_add)
        if current_credential and len(current_credential.state.roots) <= 1:
            await creds_model.remove(
                credential_id=current_credential.id,
                group_name=current_credential.group_name,
            )

    if (
        current_credential
        and credential_to_update
        and current_credential.id != credential_to_update.id
    ):
        # Add the root to another credential and delete credential if only
        # has that root
        await _remove_root_from_credential(
            root.id, root.group_name, user_email, current_credential
        )
        await update_root_ids(
            current_value=credential_to_update.state,
            modified_by=user_email,
            group_name=credential_to_update.group_name,
            credential_id=credential_to_update.id,
            root_ids=(root.id, *credential_to_update.state.roots),
        )
        if len(current_credential.state.roots) <= 1:
            await creds_model.remove(
                credential_id=current_credential.id,
                group_name=current_credential.group_name,
            )

    if current_credential is None and credential_to_update:
        # Add the root to the credential
        await update_root_ids(
            current_value=credential_to_update.state,
            modified_by=user_email,
            group_name=credential_to_update.group_name,
            credential_id=credential_to_update.id,
            root_ids=(root.id, *credential_to_update.state.roots),
        )

    if credentials is None and current_credential:
        # Delete credential from root and delete credential if only has that
        # root
        await _remove_root_from_credential(
            root.id, root.group_name, user_email, current_credential
        )
        if len(current_credential.state.roots) <= 1:
            await creds_model.remove(
                credential_id=current_credential.id,
                group_name=current_credential.group_name,
            )


async def update_git_root(  # pylint: disable=too-many-locals # noqa: MC0001
    loaders: Any,
    user_email: str,
    **kwargs: Any,
) -> Root:
    root_id: str = kwargs["id"]
    group_name = str(kwargs["group_name"]).lower()
    group: Group = await loaders.group.load(group_name)
    root: Root = await loaders.root.load((group_name, root_id))
    url: str = kwargs["url"]
    branch: str = kwargs["branch"]
    nickname: str = root.state.nickname

    validation_utils.validate_sanitized_csv_input(kwargs["environment"], url)
    if not (
        isinstance(root, GitRoot)
        and root.state.status == RootStatus.ACTIVE
        and validations.is_valid_url(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()

    if kwargs.get("nickname") and kwargs.get("nickname") != nickname:
        validation_utils.validate_sanitized_csv_input(kwargs["nickname"])
        validations.validate_nickname(kwargs["nickname"])
        validations.validate_nickname_is_unique(
            kwargs["nickname"], await loaders.group_roots.load(group_name)
        )
        nickname = kwargs["nickname"]

    if url != root.state.url:
        if await loaders.root_vulnerabilities.load(root.id):
            raise HasVulns()
        organization: Organization = await loaders.organization.load(
            group.organization_id
        )
        organization_name = organization.name
        if not validations.is_git_unique(
            url,
            branch,
            await loaders.organization_roots.load(organization_name),
        ):
            raise RepeatedRoot()

    health_check_changed: bool = (
        kwargs["includes_health_check"] != root.state.includes_health_check
    )
    if health_check_changed:
        service_enforcer = await authz.get_group_service_attributes_enforcer(
            group
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

    await _update_git_root_credentials(
        loaders=loaders,
        root=root,
        credentials=cast(Optional[Dict[str, str]], kwargs.get("credentials")),
        user_email=user_email,
    )

    new_state = GitRootState(
        branch=branch,
        environment=kwargs["environment"],
        environment_urls=root.state.environment_urls,
        git_environment_urls=[],
        gitignore=gitignore,
        includes_health_check=kwargs["includes_health_check"],
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        nickname=nickname,
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

    await send_mail_updated_root(
        loaders=loaders,
        group_name=group_name,
        root=root,
        new_state=new_state,
        user_email=user_email,
    )

    return GitRoot(
        cloning=root.cloning,
        group_name=root.group_name,
        id=root.id,
        organization_name=root.organization_name,
        state=new_state,
        type=root.type,
        unreliable_indicators=root.unreliable_indicators,
    )


async def update_ip_root(
    *,
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    if not (
        isinstance(root, IPRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    validation_utils.validate_sanitized_csv_input(nickname)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )
    new_state: IPRootState = IPRootState(
        address=root.state.address,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        nickname=nickname,
        other=None,
        port=root.state.port,
        reason=None,
        status=root.state.status,
    )

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    schedule(
        send_mail_updated_root(
            loaders=loaders,
            group_name=group_name,
            root=root,
            new_state=new_state,
            user_email=user_email,
        )
    )


async def update_url_root(
    *,
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    if not (
        isinstance(root, URLRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    validation_utils.validate_sanitized_csv_input(nickname)
    validations.validate_nickname(nickname)
    validations.validate_nickname_is_unique(
        nickname, await loaders.group_roots.load(group_name)
    )
    new_state: URLRootState = URLRootState(
        host=root.state.host,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        nickname=nickname,
        other=None,
        path=root.state.path,
        port=root.state.port,
        protocol=root.state.protocol,
        reason=None,
        status=RootStatus.ACTIVE,
    )

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    schedule(
        send_mail_updated_root(
            loaders=loaders,
            group_name=group_name,
            root=root,
            new_state=new_state,
            user_email=user_email,
        )
    )


async def send_mail_updated_root(
    *,
    loaders: Any,
    group_name: str,
    root: Root,
    new_state: Union[GitRootState, IPRootState, URLRootState],
    user_email: str,
) -> None:
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    users_email = await group_access_domain.get_users_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=Notification.ROOT_UPDATE,
        roles=roles,
    )

    old_state: Dict[str, Any] = root.state._asdict()
    new_root_content: Dict[str, Any] = {
        key: value
        for key, value in new_state._asdict().items()
        if old_state[key] != value
        and key not in ["modified_by", "modified_date"]
    }

    if new_root_content:
        await groups_mail.send_mail_updated_root(
            email_to=users_email,
            group_name=group_name,
            responsible=user_email,
            root_nickname=new_state.nickname,
            new_root_content=new_root_content,
            old_state=old_state,
            modified_date=new_state.modified_date,
        )


async def update_root_cloning_status(  # pylint: disable=too-many-arguments
    loaders: Any,
    group_name: str,
    root_id: str,
    status: GitCloningStatus,
    message: str,
    commit: Optional[str] = None,
    commit_date: Optional[str] = None,
) -> None:
    validation_utils.validate_field_length(message, 400)
    root: Root = await loaders.root.load((group_name, root_id))
    modified_date: str = datetime_utils.get_iso_date()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    await roots_model.update_git_root_cloning(
        current_value=root.cloning,
        cloning=GitRootCloning(
            modified_date=modified_date,
            reason=message,
            status=status,
            commit=commit,
            commit_date=commit_date,
        ),
        group_name=group_name,
        root_id=root_id,
    )

    group: Group = await loaders.group.load(group_name)
    is_failed: bool = (
        status == GitCloningStatus.FAILED
        and root.cloning.status == GitCloningStatus.OK
    )
    is_cloning: bool = (
        status == GitCloningStatus.OK
        and root.cloning.status == GitCloningStatus.FAILED
    )
    if (
        not root.state.use_vpn
        and group.state.status == GroupStateStatus.ACTIVE
        and (is_cloning or is_failed)
    ):
        await send_mail_root_cloning_status(
            loaders=loaders,
            group_name=group_name,
            root_nickname=root.state.nickname,
            root_id=root_id,
            modified_by=root.state.modified_by,
            modified_date=modified_date,
            is_failed=is_failed,
        )


async def send_mail_root_cloning_status(
    *,
    loaders: Any,
    group_name: str,
    root_nickname: str,
    root_id: str,
    modified_by: str,
    modified_date: str,
    is_failed: bool,
) -> None:
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    users_email = await group_access_domain.get_users_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=Notification.ROOT_UPDATE,
        roles=roles,
    )
    creation_date = await get_first_cloning_date(loaders, root_id)
    last_cloning_successful = await get_last_cloning_successful(
        loaders, root_id
    )

    await groups_mail.send_mail_root_cloning_status(
        loaders=loaders,
        email_to=users_email,
        group_name=group_name,
        last_successful_clone=last_cloning_successful,
        root_creation_date=creation_date,
        root_nickname=root_nickname,
        root_id=root_id,
        report_date=datetime_utils.get_datetime_from_iso_str(modified_date),
        modified_by=modified_by,
        is_failed=is_failed,
    )


async def activate_root(
    *, loaders: Any, group_name: str, root: Root, user_email: str
) -> None:
    new_status = RootStatus.ACTIVE

    if root.state.status != new_status:
        group: Group = await loaders.group.load(group_name)
        organization: Organization = await loaders.organization.load(
            group.organization_id
        )
        organization_name = organization.name
        org_roots = await loaders.organization_roots.load(organization_name)

        if isinstance(root, GitRoot):
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
                    git_environment_urls=[],
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

        elif isinstance(root, IPRoot):
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
                root.state.query,
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
    root: Root,
    user_email: str,
) -> None:
    new_status = RootStatus.INACTIVE

    if root.state.status != new_status:
        if isinstance(root, GitRoot):
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=GitRootState(
                    branch=root.state.branch,
                    environment=root.state.environment,
                    environment_urls=root.state.environment_urls,
                    git_environment_urls=[],
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

        elif isinstance(root, IPRoot):
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
    root: Root = await loaders.root.load((group_name, root_id))
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
    group_roots: Tuple[Root, ...],
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
    group_roots: Tuple[Root, ...], only_git_roots: bool = False
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
        if not only_git_roots or isinstance(root, GitRoot):
            root_ids[root.state.nickname] = root.id

    return root_ids


async def get_last_status_update(loaders: Any, root_id: str) -> RootState:
    """
    Returns the state item where the status last changed

    ACTIVE, [ACTIVE], INACTIVE, ACTIVE
    """
    historic_state: Tuple[
        RootState, ...
    ] = await loaders.root_historic_states.load(root_id)
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


async def get_last_cloning_successful(
    loaders: Any, root_id: str
) -> Optional[GitRootCloning]:
    """
    Returns last cloning item with "ok" state before failure

    [OK], FAILED, OK <-
    """
    historic_cloning: Tuple[
        GitRootCloning, ...
    ] = await loaders.root_historic_cloning.load(root_id)
    status_changes = tuple(
        tuple(group)
        for _, group in groupby(historic_cloning, key=attrgetter("status"))
    )

    if len(status_changes) > 2:
        last_cloning_ok = status_changes[-3]
        last_cloning: GitRootCloning = last_cloning_ok[-1]
        if last_cloning.status == "OK":
            return last_cloning

    return None


async def get_first_cloning_date(loaders: Any, root_id: str) -> str:
    historic_cloning: Tuple[
        GitRootCloning, ...
    ] = await loaders.root_historic_cloning.load(root_id)
    first_root: GitRootCloning = historic_cloning[0]

    return first_root.modified_date


async def move_root(
    loaders: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    target_group_name: str,
) -> str:
    root: Root = await loaders.root.load((group_name, root_id))
    source_group: Group = await loaders.group.load(group_name)
    source_org_id = source_group.organization_id
    target_group: Group = await loaders.group.load(target_group_name)

    if (
        root.state.status != RootStatus.ACTIVE
        or target_group_name == root.group_name
        or target_group_name
        not in await orgs_domain.get_group_names(loaders, source_org_id)
        or source_group.state.service != target_group.state.service
    ):
        raise InvalidParameter()

    target_group_roots: Tuple[Root, ...] = await loaders.group_roots.load(
        target_group_name
    )

    if isinstance(root, GitRoot):
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
    elif isinstance(root, IPRoot):
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
            root.state.query,
            target_group_roots,
        ):
            raise RepeatedRoot()

        query = "" if root.state.query is None else f"?{root.state.query}"
        path = "" if root.state.path == "/" else root.state.path
        new_root_id = await add_url_root(
            loaders,
            user_email,
            ensure_org_uniqueness=False,
            group_name=target_group_name,
            nickname=root.state.nickname,
            url=(
                f"{root.state.protocol}://{root.state.host}:{root.state.port}"
                f"{path}{query}"
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
    tzn = pytz.timezone(TIME_ZONE)
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.Session().client(**resource_options) as client:
        response = await client.describe_jobs(jobs=[job_id])
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

    execution = RootMachineExecution(
        root_id=root_id,
        job_id=job_id,
        name=current_job["jobName"],
        queue=current_job["jobQueue"].split("/")[-1],
        created_at=datetime_utils.get_as_str(queue_date),
        started_at=datetime_utils.get_as_str(start_date)
        if start_date
        else None,
        findings_executed=kwargs.pop("findings_executed", []),
        commit=kwargs.pop("git_commit", ""),
        status=kwargs.pop("status", "RUNNABLE"),
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


async def add_git_environment_secret(
    url_id: str,
    key: str,
    value: str,
    description: Optional[str] = None,
) -> bool:
    secret = Secret(
        key=key,
        value=value,
        description=description,
        created_at=datetime.now(),
    )
    return await roots_model.add_git_environment_secret(url_id, secret)


async def add_git_environment_url(  # pylint: disable=too-many-arguments
    loaders: Any,
    group_name: str,
    root_id: str,
    url: str,
    url_type: str,
    cloud_type: Optional[str] = None,
) -> bool:
    _cloud_type: Optional[GitEnvironmentCloud] = None
    try:
        _url_type = GitEnvironmentUrlType[url_type]
        if cloud_type:
            _cloud_type = GitEnvironmentCloud[cloud_type]
    except KeyError as exc:
        raise InvalidField("type") from exc

    await loaders.root.load((group_name, root_id))
    environment = GitEnvironmentUrl(
        id=hashlib.sha1(url.encode()).hexdigest(),  # nosec
        created_at=datetime.now(),
        url=url,
        url_type=_url_type,
        cloud_type=_cloud_type,
    )
    return await roots_model.add_git_environment_url(root_id, url=environment)


async def remove_environment_url(root_id: str, url: str) -> None:
    await roots_model.remove_environment_url(
        root_id, url_id=hashlib.sha1(url.encode()).hexdigest()  # nosec
    )


async def send_mail_environment(  # pylint: disable=too-many-arguments
    loaders: Any,
    date: str,
    group_name: str,
    git_root: str,
    urls_added: List[str],
    urls_deleted: List[str],
    user_email: str,
    other: Optional[str],
    reason: Optional[str],
) -> None:
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    users_email = await group_access_domain.get_users_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=Notification.ROOT_UPDATE,
        roles=roles,
    )

    await groups_mail.send_mail_environment_report(
        email_to=users_email,
        group_name=group_name,
        responsible=user_email,
        git_root=git_root,
        urls_added=urls_added,
        urls_deleted=urls_deleted,
        modified_date=date,
        other=other,
        reason=reason,
    )


async def remove_secret(root_id: str, secret_key: str) -> None:
    await roots_model.remove_secret(root_id, secret_key)


async def remove_environment_url_secret(url_id: str, secret_key: str) -> None:
    await roots_model.remove_environment_url_secret(url_id, secret_key)


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
    url: str = format_git_repo_url(kwargs["url"])
    cred_type: CredentialType = CredentialType(kwargs["credentials"]["type"])
    if key := kwargs["credentials"].get("key"):
        kwargs["credentials"]["key"] = _format_credential_key(cred_type, key)
    await validations.validate_git_credentials(
        url, cred_type, kwargs["credentials"]
    )
