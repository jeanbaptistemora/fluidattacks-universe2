# pylint: disable=too-many-lines

import aioboto3
from aioextensions import (
    collect,
    schedule,
)
from asyncio.tasks import (
    sleep,
)
import authz
from batch.dal import (
    get_actions_by_name,
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    PutActionResult,
)
from collections import (
    defaultdict,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_AWS_REGION_NAME,
    FI_ENVIRONMENT,
)
from custom_exceptions import (
    CredentialNotFound,
    FileNotFound,
    HasVulns,
    InvalidField,
    InvalidParameter,
    InvalidRootExclusion,
    InvalidRootType,
    PermissionDenied,
    RepeatedRoot,
    RequiredCredentials,
    RootAlreadyCloning,
    RootEnvironmentUrlNotFound,
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as creds_model,
    roots as roots_model,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    CredentialsState,
    HttpsPatSecret,
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.groups.enums import (
    GroupStateStatus,
    GroupSubscriptionType,
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
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    Root,
    RootEnvironmentCloud,
    RootEnvironmentUrl,
    RootEnvironmentUrlType,
    RootMachineExecution,
    RootRequest,
    RootState,
    RootUnreliableIndicators,
    Secret,
    URLRoot,
    URLRootState,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import git_self
from git_self import (
    ssh_ls_remote,
)
import hashlib
from itertools import (
    chain,
    groupby,
)
import json
import logging
from mailer import (
    groups as groups_mail,
    utils as mailer_utils,
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
    utils as orgs_utils,
    validations as orgs_validations,
)
import pytz
import re
from roots import (
    utils as roots_utils,
    validations,
)
from s3 import (
    operations as s3_operations,
)
from settings.various import (
    TIME_ZONE,
)
from typing import (
    Any,
    cast,
)
from urllib3.exceptions import (
    LocationParseError,
)
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    ParseResult,
    urlparse,
)
from uuid import (
    uuid4,
)

LOGGER = logging.getLogger(__name__)
RESTRICTED_REPO_URLS = ["https://gitlab.com/fluidattacks/universe"]


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


async def get_root(
    loaders: Dataloaders, root_id: str, group_name: str
) -> Root:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not root:
        raise RootNotFound()

    return root


async def _get_credentials_type_to_add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    organization: Organization,
    group: Group,
    url: str,
    branch: str,
    credentials: dict[str, str] | None,
    required_credentials: bool,
    user_email: str,
    use_vpn: bool,
) -> Credentials | None:
    organization_credential: Credentials | None = None
    if required_credentials and not credentials:
        raise RequiredCredentials()

    if credentials:
        if (credential_id := credentials.get("id")) and credential_id:
            await validations.validate_credential_in_organization(
                loaders,
                credential_id,
                group.organization_id,
            )
            organization_credential = await loaders.credentials.load(
                CredentialsRequest(
                    id=credential_id,
                    organization_id=group.organization_id,
                )
            )
            if not use_vpn and required_credentials:
                await validations.working_credentials(
                    url, branch, organization_credential, loaders
                )
        else:
            organization_credential = _format_root_credential_new(
                credentials, organization.id, user_email
            )
            await orgs_validations.validate_credentials_name_in_organization(
                loaders,
                organization_credential.organization_id,
                organization_credential.state.name,
            )
            if not use_vpn and required_credentials:
                await validations.working_credentials(
                    url, branch, organization_credential, loaders
                )
            await creds_model.add(credential=organization_credential)

    return organization_credential


def _is_allowed(url: str) -> bool:
    if FI_ENVIRONMENT == "development":
        return True
    return url not in RESTRICTED_REPO_URLS


@validation_utils.validate_field_exist_deco("environment")
@validation_utils.validate_fields_deco(["url"])
@validation_utils.validate_sanitized_csv_input_deco(
    ["nickname", "url", "environment"]
)
@validations.validate_nickname_deco("nickname")
async def add_git_root(  # pylint: disable=too-many-locals
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    required_credentials: bool = False,
    **kwargs: Any,
) -> GitRoot:
    group_name = str(kwargs["group_name"]).lower()
    group: Group = await loaders.group.load(group_name)
    url: str = roots_utils.format_git_repo_url(kwargs["url"])
    branch: str = kwargs["branch"].rstrip()
    loaders.group_roots.clear(group_name)
    nickname: str = _assign_nickname(
        nickname="",
        new_nickname=_format_root_nickname(kwargs.get("nickname", ""), url),
        roots=await loaders.group_roots.load(group_name),
    )
    use_vpn: bool = kwargs.get("use_vpn", False)

    if not (
        validations.is_valid_url(url)
        and _is_allowed(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()
    includes_health_check = kwargs["includes_health_check"]
    service_enforcer = authz.get_group_service_attributes_enforcer(group)
    if includes_health_check and not service_enforcer("has_squad"):
        raise PermissionDenied()

    gitignore = kwargs["gitignore"]
    group_enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if gitignore and not group_enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    if (
        ensure_org_uniqueness
        and group.state.type != GroupSubscriptionType.ONESHOT
        and not validations.is_git_unique(
            url,
            branch,
            group_name,
            await loaders.organization_roots.load(organization.name),
            include_inactive=True,
        )
    ):
        raise RepeatedRoot()

    root_id = str(uuid4())
    credentials: dict[str, str] | None = kwargs.get("credentials")

    organization_credential = await _get_credentials_type_to_add(
        loaders=loaders,
        organization=organization,
        group=group,
        branch=branch,
        url=url,
        credentials=credentials,
        required_credentials=required_credentials,
        user_email=user_email,
        use_vpn=use_vpn,
    )
    modified_date = datetime_utils.get_utc_now()
    root = GitRoot(
        cloning=GitRootCloning(
            modified_date=modified_date,
            reason="root created",
            status=GitCloningStatus("UNKNOWN"),
        ),
        created_by=user_email,
        created_date=modified_date,
        group_name=group_name,
        id=root_id,
        organization_name=organization.name,
        state=GitRootState(
            branch=branch,
            credential_id=organization_credential.id
            if organization_credential
            else None,
            environment=kwargs["environment"],
            gitignore=gitignore,
            includes_health_check=includes_health_check,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            reason=None,
            status=RootStatus.ACTIVE,
            url=url,
            use_vpn=use_vpn,
        ),
        type=RootType.GIT,
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
    )
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
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    address: str = kwargs["address"]
    if not validations.is_valid_ip(address):
        raise InvalidParameter()

    group: Group = await loaders.group.load(group_name)
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    organization_name = organization.name
    if (
        ensure_org_uniqueness
        and group.state.type != GroupSubscriptionType.ONESHOT
        and not validations.is_ip_unique(
            address,
            await loaders.organization_roots.load(organization_name),
            include_inactive=True,
        )
    ):
        raise RepeatedRoot()

    loaders.group_roots.clear(group_name)
    nickname = _assign_nickname(
        new_nickname=kwargs["nickname"],
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )

    modified_date = datetime_utils.get_utc_now()
    root = IPRoot(
        created_by=user_email,
        created_date=modified_date,
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
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


@validation_utils.validate_fields_deco(["url"])
@validation_utils.validate_sanitized_csv_input_deco(["url", "nickname"])
@validation_utils.validate_url_deco("url")
async def add_url_root(  # pylint: disable=too-many-locals
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    loaders.group_roots.clear(group_name)
    nickname: str = _assign_nickname(
        nickname="",
        new_nickname=kwargs["nickname"],
        roots=await loaders.group_roots.load(group_name),
    )
    url: str = str(kwargs["url"])

    try:
        url_attributes = parse_url(url)
    except LocationParseError as ex:
        raise InvalidParameter() from ex

    if not url_attributes.host or url_attributes.scheme not in {
        "http",
        "https",
        "file",
    }:
        raise InvalidParameter()

    host: str = url_attributes.host
    fragment: str | None = url_attributes.fragment
    path: str = url_attributes.path or "/"
    query: str | None = url_attributes.query
    default_port = "443" if url_attributes.scheme == "https" else "80"
    port = str(url_attributes.port) if url_attributes.port else default_port
    protocol: str = url_attributes.scheme.upper()

    group: Group = await loaders.group.load(group_name)
    if protocol == "FILE":
        fragment = None
        query = None
        port = "0"
        if host not in {file.file_name for file in group.files or []}:
            raise FileNotFound()

    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    organization_name = organization.name
    if fragment:
        path = f"{path}#{fragment}"

    if (
        ensure_org_uniqueness
        and group.state.type != GroupSubscriptionType.ONESHOT
        and not validations.is_url_unique(
            host,
            path,
            port,
            protocol,
            query,
            tuple(await loaders.organization_roots.load(organization_name)),
            include_inactive=True,
        )
    ):
        raise RepeatedRoot()

    modified_date = datetime_utils.get_utc_now()
    root = URLRoot(
        created_by=user_email,
        created_date=modified_date,
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


def _format_root_credential_new(
    credentials: dict[str, str], organization_id: str, user_email: str
) -> Credentials:
    credential_name = credentials["name"]
    credential_type = CredentialType(credentials["type"])
    is_pat: bool = bool(credentials.get("is_pat", False))

    if not credential_name:
        raise InvalidParameter()
    if is_pat:
        if "azure_organization" not in credentials:
            raise InvalidParameter("azure_organization")
        validation_utils.validate_space_field(
            credentials["azure_organization"]
        )
    if not is_pat and "azure_organization" in credentials:
        raise InvalidParameter("azure_organization")

    secret = orgs_utils.format_credentials_secret_type(credentials)

    return Credentials(
        id=str(uuid4()),
        organization_id=organization_id,
        owner=user_email,
        state=CredentialsState(
            modified_by=user_email,
            modified_date=datetime_utils.get_utc_now(),
            name=credentials["name"],
            secret=secret,
            type=credential_type,
            is_pat=is_pat,
            azure_organization=credentials["azure_organization"]
            if is_pat
            else None,
        ),
    )


async def update_git_environments(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: list[str],
    reason: str | None,
    other: str | None,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    modified_date = datetime_utils.get_utc_now()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    is_valid: bool = root.state.status == RootStatus.ACTIVE and all(
        validations.is_valid_url(url) for url in environment_urls
    )
    if not is_valid:
        raise InvalidParameter()

    root_urls = await loaders.root_environment_urls.load(root_id)
    urls = {
        url.url
        for url in root_urls
        if url.url_type == RootEnvironmentUrlType.URL
    }
    urls_deleted: list[str] = list(set(urls).difference(set(environment_urls)))
    urls_added: list[str] = [
        url for url in environment_urls if url not in urls
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
            add_root_environment_url(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                url=url,
                url_type="URL",
                user_email=user_email,
            )
            for url in urls_added
        ]
    )

    if urls_added or urls_deleted:
        schedule(
            send_mail_environment(
                loaders=loaders,
                modified_date=modified_date,
                group_name=group_name,
                git_root=root.state.nickname,
                git_root_url=root.state.url,
                urls_added=urls_added,
                urls_deleted=urls_deleted,
                user_email=user_email,
                other=other,
                reason=reason,
            )
        )


async def _update_git_root_credentials(  # noqa: MC0001
    loaders: Dataloaders,
    group: Group,
    root: GitRoot,
    credentials: dict[str, str] | None,
    user_email: str,
) -> str | None:
    credential_id = credentials.get("id") if credentials else None
    credential_to_add: Credentials | None = None
    if credentials and credential_id is None:
        credential_to_add = _format_root_credential_new(
            credentials, group.organization_id, user_email
        )

    if not credential_to_add and credential_id is None:
        return None

    if credential_to_add and credential_id is None:
        await orgs_validations.validate_credentials_name_in_organization(
            loaders,
            credential_to_add.organization_id,
            credential_to_add.state.name,
        )
        await creds_model.add(credential=credential_to_add)
        return credential_to_add.id

    if credential_id is not None:
        await validations.validate_credential_in_organization(
            loaders,
            credential_id,
            group.organization_id,
        )
        return credential_id
    return root.state.credential_id


def _validate_git_root_url(root: GitRoot, gitignore: list[str]) -> None:
    if not validations.is_exclude_valid(gitignore, root.state.url):
        raise InvalidRootExclusion()


@validation_utils.validate_sanitized_csv_input_deco(["new_nickname"])
@validations.validate_nickname_deco("new_nickname")
@validations.validate_nickname_is_unique_deco(
    nickname_field="new_nickname",
    roots_fields="roots",
    old_nickname_field="nickname",
)
def _assign_nickname(  # pylint: disable=unused-argument
    nickname: str, new_nickname: str, roots: Iterable[Root]
) -> str:
    if new_nickname and new_nickname != nickname:
        return new_nickname
    return nickname


@validations.validate_git_root_deco("root")
@validations.validate_active_root_deco("root")
def _check_repeated_root(
    *,
    url: str,
    branch: str,
    group_name: str,
    root: GitRoot,
    root_vulnerabilities: Any,
    organization_roots: Iterable[Root],
) -> None:
    if url != root.state.url:
        if root_vulnerabilities:
            raise HasVulns()
        if not validations.is_git_unique(
            url,
            branch,
            group_name,
            organization_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()


@validation_utils.validate_field_exist_deco("environment")
@validation_utils.validate_fields_deco(["url"])
@validation_utils.validate_sanitized_csv_input_deco(["url", "environment"])
@validations.validate_url_branch_deco(url_field="url", branch_field="branch")
async def update_git_root(  # pylint: disable=too-many-locals # noqa: MC0001
    loaders: Dataloaders,
    user_email: str,
    **kwargs: Any,
) -> Root:
    root_id: str = kwargs["id"]
    group_name = str(kwargs["group_name"]).lower()
    group: Group = await loaders.group.load(group_name)
    root: GitRoot = cast(GitRoot, await get_root(loaders, root_id, group_name))
    url: str = kwargs["url"]
    branch: str = kwargs["branch"]

    nickname = _assign_nickname(
        nickname=root.state.nickname,
        new_nickname=kwargs.get("nickname"),
        roots=await loaders.group_roots.load(group_name),
    )

    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    _check_repeated_root(
        url=url,
        branch=branch,
        group_name=group_name,
        root=root,
        root_vulnerabilities=await loaders.root_vulnerabilities.load(root.id),
        organization_roots=await loaders.organization_roots.load(
            organization.name
        ),
    )

    health_check_changed: bool = (
        kwargs["includes_health_check"] != root.state.includes_health_check
    )
    if health_check_changed:
        service_enforcer = authz.get_group_service_attributes_enforcer(group)
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
    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if gitignore != root.state.gitignore and not enforcer(
        group_name, "update_git_root_filter"
    ):
        raise PermissionDenied()
    _validate_git_root_url(root, gitignore)

    credentials: dict[str, str] | None = kwargs.get("credentials")
    credential_id = await _update_git_root_credentials(
        loaders=loaders,
        group=group,
        root=root,
        credentials=credentials,
        user_email=user_email,
    )

    new_state = GitRootState(
        branch=branch,
        credential_id=credential_id,
        environment=kwargs["environment"],
        gitignore=gitignore,
        includes_health_check=kwargs["includes_health_check"],
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
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
        created_by=root.created_by,
        created_date=root.created_date,
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
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not (
        isinstance(root, IPRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    _assign_nickname(
        new_nickname=nickname,
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )
    new_state: IPRootState = IPRootState(
        address=root.state.address,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        nickname=nickname,
        other=None,
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
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not (
        isinstance(root, URLRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    _assign_nickname(
        new_nickname=nickname,
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )
    new_state: URLRootState = URLRootState(
        host=root.state.host,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
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
    loaders: Dataloaders,
    group_name: str,
    root: Root,
    new_state: GitRootState | IPRootState | URLRootState,
    user_email: str,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="updated_root",
    )

    old_state: dict[str, Any] = root.state._asdict()
    new_root_content: dict[str, Any] = {
        key: value
        for key, value in new_state._asdict().items()
        if old_state[key] != value
        and key not in ["modified_by", "modified_date", "credential_id"]
    }

    if new_root_content:
        await groups_mail.send_mail_updated_root(
            loaders=loaders,
            email_to=users_email,
            group_name=group_name,
            responsible=user_email,
            root_nickname=new_state.nickname,
            new_root_content=new_root_content,
            old_state=old_state,
            modified_date=new_state.modified_date,
        )


@validation_utils.validate_field_length_deco("message", 400)
async def update_root_cloning_status(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    status: GitCloningStatus,
    message: str,
    commit: str | None = None,
    commit_date: datetime | None = None,
) -> None:
    root = await get_root(loaders, root_id, group_name)
    modified_date = datetime_utils.get_utc_now()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    # As this operation can fail due to optimistic locking to avoid concurrency
    # issues (esp. the modified date being slightly different in fractions of
    # a second) a retry backup is needed
    try:
        await roots_model.update_git_root_cloning(
            current_value=root.cloning,
            cloning=GitRootCloning(
                modified_date=modified_date,
                reason=message,
                status=status,
                commit=commit,
                commit_date=commit_date,
            ),
            repo_nickname=root.state.nickname,
            group_name=group_name,
            root_id=root_id,
        )
    except ConditionalCheckFailedException:
        await sleep(1.0)
        loaders.root.clear(RootRequest(group_name, root_id))
        git_root = cast(
            GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
        )
        await roots_model.update_git_root_cloning(
            current_value=git_root.cloning,
            cloning=GitRootCloning(
                modified_date=modified_date,
                reason=message,
                status=status,
                commit=commit,
                commit_date=commit_date,
            ),
            repo_nickname=root.state.nickname,
            group_name=group_name,
            root_id=root_id,
        )

    if validate_error_message(message):
        await send_mail_root_cloning_failed(
            loaders=loaders,
            group_name=group_name,
            modified_date=modified_date,
            root=root,
            status=status,
        )


def validate_error_message(
    message: str,
) -> bool:
    errors_list: list[str] = [
        "fatal: not a git repository",
        "fatal: HTTP request failed",
        "error: branch ‘remotes/origin/ABC’ not found",
        "fatal: authentication failed",
        "remote: Invalid username or password",
        "Permission denied (publickey)",
    ]
    for error in errors_list:
        if error in message:
            return True
    return False


async def send_mail_root_cloning_failed(
    *,
    loaders: Dataloaders,
    group_name: str,
    modified_date: datetime,
    root: Root,
    status: GitCloningStatus,
) -> None:
    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    loaders.group.clear(group_name)
    group: Group = await loaders.group.load(group_name)
    is_failed_status_cloning: bool = await is_failed_cloning(loaders, root.id)
    is_failed: bool = (
        status == GitCloningStatus.FAILED and is_failed_status_cloning
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
            root_id=root.id,
            modified_by=root.state.modified_by,
            modified_date=modified_date,
            is_failed=is_failed,
        )


async def send_mail_root_cloning_status(
    *,
    loaders: Dataloaders,
    group_name: str,
    root_nickname: str,
    root_id: str,
    modified_by: str,
    modified_date: datetime,
    is_failed: bool,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="root_cloning_status",
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
        report_date=modified_date,
        modified_by=modified_by,
        is_failed=is_failed,
    )


async def activate_root(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    root: Root,
) -> None:
    new_status = RootStatus.ACTIVE

    if root.state.status != new_status:
        group: Group = await loaders.group.load(group_name)
        organization = await orgs_utils.get_organization(
            loaders, group.organization_id
        )
        organization_name = organization.name
        org_roots = await loaders.organization_roots.load(organization_name)

        if isinstance(root, GitRoot):
            if not validations.is_git_unique(
                root.state.url,
                root.state.branch,
                root.group_name,
                org_roots,
            ):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=GitRootState(
                    branch=root.state.branch,
                    credential_id=root.state.credential_id,
                    environment=root.state.environment,
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
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
                    requester_email=email,
                )

        elif isinstance(root, IPRoot):
            if not validations.is_ip_unique(root.state.address, org_roots):
                raise RepeatedRoot()

            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    address=root.state.address,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=None,
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
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
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
    email: str,
    group_name: str,
    other: str | None,
    reason: str,
    root: Root,
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
                    credential_id=root.state.credential_id,
                    environment=root.state.environment,
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
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
                    requester_email=email,
                )

        elif isinstance(root, IPRoot):
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    address=root.state.address,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=other,
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
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=other,
                    path=root.state.path,
                    port=root.state.port,
                    protocol=root.state.protocol,
                    reason=reason,
                    status=new_status,
                ),
            )


def get_root_id_by_nickname(
    nickname: str,
    group_roots: Iterable[Root],
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
    root_ids_by_nicknames: dict[str, str],
) -> str:
    try:
        root_id = root_ids_by_nicknames[nickname]
    except KeyError as exc:
        raise RootNotFound() from exc

    return root_id


def get_root_ids_by_nicknames(
    group_roots: Iterable[Root], only_git_roots: bool = False
) -> dict[str, str]:
    # Get a dict that have the relation between nickname and id for roots
    # There are roots with the same nickname
    # then It is going to take the active root first
    sorted_active_roots = sorted(
        [
            root
            for root in group_roots
            if root.state.status == RootStatus.ACTIVE
        ],
        key=lambda root: root.state.modified_date,
        reverse=False,
    )
    sorted_inactive_roots = sorted(
        [
            root
            for root in group_roots
            if root.state.status == RootStatus.INACTIVE
        ],
        key=lambda root: root.state.modified_date,
        reverse=False,
    )
    root_ids: dict[str, str] = {}
    for root in sorted_inactive_roots + sorted_active_roots:
        if not only_git_roots or isinstance(root, GitRoot):
            root_ids[root.state.nickname] = root.id

    return root_ids


async def get_last_status_update(
    loaders: Dataloaders, root_id: str
) -> RootState:
    """
    Returns the state item where the status last changed

    ACTIVE, [ACTIVE], INACTIVE, ACTIVE
    """
    historic_state = await loaders.root_historic_states.load(root_id)
    status_changes = tuple(
        tuple(group)
        for _, group in groupby(historic_state, key=attrgetter("status"))
    )
    with_current_status = status_changes[-1]

    return with_current_status[0]


async def get_last_status_update_date(
    loaders: Dataloaders, root_id: str
) -> datetime:
    """Returns the date where the status last changed"""
    last_status_update = await get_last_status_update(loaders, root_id)

    return last_status_update.modified_date


async def historic_cloning_grouped(
    loaders: Dataloaders, root_id: str
) -> tuple[tuple[GitRootCloning, ...], ...]:
    """Returns the history of cloning failures and successes grouped"""
    loaders.root_historic_cloning.clear(root_id)
    historic_cloning = await loaders.root_historic_cloning.load(root_id)
    filtered_historic_cloning: tuple[GitRootCloning, ...] = tuple(
        filter(
            lambda cloning: cloning.status
            in [GitCloningStatus.OK, GitCloningStatus.FAILED],
            historic_cloning,
        )
    )
    grouped_historic_cloning = tuple(
        tuple(group)
        for _, group in groupby(
            filtered_historic_cloning, key=attrgetter("status")
        )
    )

    return grouped_historic_cloning


async def get_last_cloning_successful(
    loaders: Dataloaders, root_id: str
) -> GitRootCloning | None:
    """
    Returns last cloning item with "ok" state before failure

    [OK], FAILED, OK <-
    """

    status_changes = await historic_cloning_grouped(loaders, root_id)

    if len(status_changes) > 2:
        last_cloning_ok = status_changes[-3]
        last_cloning: GitRootCloning = last_cloning_ok[-1]
        if last_cloning.status == "OK":
            return last_cloning

    return None


async def is_failed_cloning(loaders: Dataloaders, root_id: str) -> bool:
    """
    Returns if last historic cloning has failed two times

    OK, FAILED, FAILED
    """
    status_changes = await historic_cloning_grouped(loaders, root_id)
    has_failed: bool = False

    if len(status_changes) > 1:
        last_cloning_failed = status_changes[-1]
        last_cloning: GitRootCloning = last_cloning_failed[-1]
        has_failed = (
            last_cloning.status == GitCloningStatus.FAILED
            and len(last_cloning_failed) == 2
        )

    return has_failed


async def get_first_cloning_date(
    loaders: Dataloaders, root_id: str
) -> datetime:
    historic_cloning = await loaders.root_historic_cloning.load(root_id)
    first_root: GitRootCloning = historic_cloning[0]

    return first_root.modified_date


async def move_root(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    root_id: str,
    target_group_name: str,
) -> str:
    root = await get_root(loaders, root_id, group_name)
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

    target_group_roots = await loaders.group_roots.load(target_group_name)

    if isinstance(root, GitRoot):
        if not validations.is_git_unique(
            root.state.url,
            root.state.branch,
            target_group_name,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        new_root = await add_git_root(
            loaders,
            email,
            ensure_org_uniqueness=False,
            branch=root.state.branch,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            group_name=target_group_name,
            includes_health_check=root.state.includes_health_check,
            nickname=root.state.nickname,
            url=root.state.url,
            credentials=(
                {"id": root.state.credential_id}
                if root.state.credential_id
                else None
            ),
        )
        new_root_id = new_root.id
    elif isinstance(root, IPRoot):
        if not validations.is_ip_unique(
            root.state.address,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        new_root_id = await add_ip_root(
            loaders,
            email,
            ensure_org_uniqueness=False,
            address=root.state.address,
            group_name=target_group_name,
            nickname=root.state.nickname,
        )
    else:
        if not validations.is_url_unique(
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol,
            root.state.query,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        query = "" if root.state.query is None else f"?{root.state.query}"
        path = "" if root.state.path == "/" else root.state.path
        new_root_id = await add_url_root(
            loaders=loaders,
            user_email=email,
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
        email=email,
    )

    return new_root_id


async def add_machine_execution(
    root_id: str,
    job_id: str,
    **kwargs: Any,
) -> bool:
    tzn = pytz.timezone(TIME_ZONE)
    options = dict(
        region_name=FI_AWS_REGION_NAME,
        service_name="batch",
    )
    async with aioboto3.Session().client(**options) as client:
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
        created_at=queue_date,
        started_at=start_date,
        findings_executed=kwargs.pop("findings_executed", []),
        commit=kwargs.pop("git_commit", ""),
        status=kwargs.pop("status", "RUNNABLE"),
    )
    return await roots_model.add_machine_execution(root_id, execution)


async def add_secret(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    key: str,
    value: str,
    description: str | None = None,
) -> bool:
    await loaders.root.load(RootRequest(group_name, root_id))
    secret = Secret(key=key, value=value, description=description)
    return await roots_model.add_secret(root_id, secret)


async def add_root_environment_secret(
    url_id: str,
    key: str,
    value: str,
    description: str | None = None,
) -> bool:
    secret = Secret(
        key=key,
        value=value,
        description=description,
        created_at=datetime.now(),
    )
    return await roots_model.add_root_environment_secret(url_id, secret)


async def _add_secrets_aws(environment_id: str) -> None:
    await add_root_environment_secret(
        environment_id,
        key="AWS_ACCESS_KEY_ID",
        value="",
        description="AWS access keys to make programmatic calls to AWS",
    )
    await add_root_environment_secret(
        environment_id,
        key="AWS_SECRET_ACCESS_KEY",
        value="",
        description="AWS secret access keys to make programmatic calls to AWS",
    )


async def add_root_environment_url(
    *,
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    url: str,
    url_type: str,
    user_email: str,
    should_notified: bool = False,
    cloud_type: str | None = None,
) -> bool:
    _cloud_type: RootEnvironmentCloud | None = None
    try:
        _url_type = RootEnvironmentUrlType[url_type]
        if cloud_type:
            _cloud_type = RootEnvironmentCloud[cloud_type]
    except KeyError as exc:
        raise InvalidField("urlType") from exc

    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not isinstance(root, GitRoot):
        raise InvalidRootType()

    environment = RootEnvironmentUrl(
        id=hashlib.sha1(url.encode()).hexdigest(),  # nosec
        created_at=datetime.now(),
        created_by=user_email,
        url=url,
        url_type=_url_type,
        cloud_name=_cloud_type,
    )
    result_environment = await roots_model.add_root_environment_url(
        root_id, url=environment
    )
    if not result_environment:
        return False

    if cloud_type and cloud_type == RootEnvironmentCloud.AWS:
        await _add_secrets_aws(environment.id)

    if should_notified:
        schedule(
            send_mail_environment(
                loaders=loaders,
                modified_date=datetime_utils.get_utc_now(),
                group_name=group_name,
                git_root=root.state.nickname,
                git_root_url=root.state.url,
                urls_added=[url],
                urls_deleted=[],
                user_email=user_email,
                other=None,
                reason=None,
            )
        )
    return True


async def remove_environment_url(root_id: str, url: str) -> None:
    await roots_model.remove_environment_url(
        root_id, url_id=hashlib.sha1(url.encode()).hexdigest()  # nosec
    )


async def send_mail_environment(
    *,
    loaders: Dataloaders,
    modified_date: datetime,
    group_name: str,
    git_root: str,
    git_root_url: str,
    urls_added: list[str],
    urls_deleted: list[str],
    user_email: str,
    other: str | None = None,
    reason: str | None = None,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="environment_report",
    )

    await groups_mail.send_mail_environment_report(
        loaders=loaders,
        email_to=users_email,
        group_name=group_name,
        responsible=user_email,
        git_root=git_root,
        git_root_url=git_root_url,
        urls_added=urls_added,
        urls_deleted=urls_deleted,
        modified_date=modified_date,
        other=other,
        reason=reason,
    )


async def remove_environment_url_id(
    *,
    loaders: Dataloaders,
    root_id: str,
    url_id: str,
    user_email: str,
    group_name: str,
) -> str:
    urls = await loaders.root_environment_urls.load(root_id)
    url: str | None = next(
        (env_url.url for env_url in urls if env_url.id == url_id),
        None,
    )
    if url is None:
        raise RootEnvironmentUrlNotFound()

    await roots_model.remove_environment_url(root_id, url_id=url_id)

    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not isinstance(root, GitRoot):
        raise InvalidRootType()

    schedule(
        send_mail_environment(
            loaders=loaders,
            modified_date=datetime_utils.get_utc_now(),
            group_name=group_name,
            git_root=root.state.nickname,
            git_root_url=root.state.url,
            urls_added=[],
            urls_deleted=[url],
            user_email=user_email,
            other=None,
            reason=None,
        )
    )

    return url


async def remove_secret(root_id: str, secret_key: str) -> None:
    await roots_model.remove_secret(root_id, secret_key)


async def remove_environment_url_secret(url_id: str, secret_key: str) -> None:
    await roots_model.remove_environment_url_secret(url_id, secret_key)


async def is_in_s3(group_name: str, root_nickname: str) -> bool:
    return bool(
        await s3_operations.list_files(
            f"continuous-repositories/{group_name}/{root_nickname}.tar.gz",
        )
    )


async def remove_root(
    *,
    email: str,
    group_name: str,
    reason: str,
    root: Root,
) -> None:
    await deactivate_root(
        group_name=group_name,
        other="",
        reason=reason,
        root=root,
        email=email,
    )
    await roots_model.remove(root_id=root.id)
    LOGGER.info(
        "Root removed",
        extra={
            "extra": {
                "root_id": root.id,
                "group_name": root.group_name,
            }
        },
    )


async def get_unsolved_events_by_root(
    loaders: Dataloaders, group_name: str
) -> dict[str, tuple[Event, ...]]:
    unsolved_events_by_root: defaultdict[
        str | None, list[Event]
    ] = defaultdict(list[Event])
    unsolved_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name, is_solved=False)
    )
    for event in unsolved_events:
        unsolved_events_by_root[event.root_id].append(event)
    return {
        root_id: tuple(events)
        for root_id, events in unsolved_events_by_root.items()
        if root_id
    }


async def _ls_remote_root(
    root: GitRoot, cred: Credentials, loaders: Dataloaders
) -> str | None:
    last_commit: str | None

    if root.state.use_vpn:
        last_commit = None
    elif isinstance(cred.state.secret, SshSecret):
        last_commit = await ssh_ls_remote(
            repo_url=root.state.url, credential_key=cred.state.secret.key
        )
    elif isinstance(cred.state.secret, HttpsSecret):
        last_commit = await git_self.https_ls_remote(
            repo_url=root.state.url,
            user=cred.state.secret.user,
            password=cred.state.secret.password,
        )
    elif isinstance(cred.state.secret, HttpsPatSecret):
        last_commit = await git_self.https_ls_remote(
            repo_url=root.state.url,
            token=cred.state.secret.token,
        )
    elif isinstance(
        cred.state.secret,
        (
            OauthGithubSecret,
            OauthAzureSecret,
            OauthGitlabSecret,
            OauthBitbucketSecret,
        ),
    ):
        token = await validations.get_cred_token(
            loaders=loaders,
            organization_id=cred.organization_id,
            credential_id=cred.id,
        )
        last_commit = await git_self.https_ls_remote(
            repo_url=root.state.url,
            token=token,
            is_oauth=True,
            provider=roots_utils.get_oauth_type(cred),
        )
    else:
        raise InvalidParameter()

    return last_commit


def _filter_active_roots_with_credentials(
    roots: Iterable[GitRoot], use_vpn: bool
) -> tuple[GitRoot, ...]:
    valid_roots: tuple[GitRoot, ...] = tuple(
        root
        for root in roots
        if (
            root.state.status == RootStatus.ACTIVE
            and root.state.use_vpn == use_vpn
        )
    )
    if any(root.state.credential_id is None for root in roots):
        raise CredentialNotFound()

    return valid_roots


async def _filter_roots_unsolved_events(
    roots: tuple[GitRoot, ...], loaders: Dataloaders, group_name: str
) -> tuple[GitRoot, ...]:
    unsolved_events_by_root: dict[
        str, tuple[Event, ...]
    ] = await get_unsolved_events_by_root(loaders, group_name)
    roots_with_unsolved_events: tuple[str, ...] = tuple(
        root.id for root in roots if root.id in unsolved_events_by_root
    )
    await collect(
        [
            update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                status=GitCloningStatus.FAILED,
                message="Git root has unsolved events",
            )
            for root_id in roots_with_unsolved_events
        ]
    )

    return tuple(
        root for root in roots if root.id not in roots_with_unsolved_events
    )


async def _filter_roots_already_in_queue(
    roots: Iterable[GitRoot], group_name: str
) -> tuple[GitRoot, ...]:
    clone_queue = await get_actions_by_name("clone_roots", group_name)
    root_nicknames_in_queue = set(
        chain.from_iterable(
            [
                json.loads(clone_job.additional_info)["roots"]
                for clone_job in clone_queue
            ]
        )
    )
    valid_roots = tuple(
        root
        for root in roots
        if root.state.nickname not in root_nicknames_in_queue
    )
    if not valid_roots:
        raise RootAlreadyCloning()

    return valid_roots


async def _filter_roots_working_creds(  # pylint: disable=too-many-arguments
    roots: Iterable[GitRoot],
    loaders: Dataloaders,
    group_name: str,
    organization_id: str,
    force: bool,
    queue_with_vpn: bool,
) -> tuple[GitRoot, ...]:
    roots_credentials = await loaders.credentials.load_many(
        [
            CredentialsRequest(
                id=root.state.credential_id,
                organization_id=organization_id,
            )
            for root in roots
            if root.state.credential_id is not None
        ]
    )
    roots_last_commits = await collect(
        (
            get_commit_last_sucessful_clone(loaders=loaders, root=root)
            for root in roots
        ),
        workers=15,
    )

    last_root_commits_in_s3: tuple[
        tuple[GitRoot, str | None, str | None, bool], ...
    ] = tuple(
        zip(
            roots,
            roots_last_commits,
            tuple(
                await collect(
                    _ls_remote_root(root, credential, loaders)
                    for root, credential in zip(roots, roots_credentials)
                    if credential
                )
            ),
            tuple(
                await collect(
                    is_in_s3(group_name, root.state.nickname) for root in roots
                )
            ),
        )
    )

    roots_with_issues: tuple[tuple[GitRoot, str | None], ...] = tuple(
        (root, last_commit)
        for root, last_commit, commit, _ in last_root_commits_in_s3
        if commit is None and not root.state.use_vpn
    )
    await collect(
        [
            update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.FAILED,
                message="Credentials does not work",
                commit=last_commit,
            )
            for root, last_commit in roots_with_issues
        ]
    )

    unchanged_roots: tuple[tuple[GitRoot, str | None], ...] = tuple(
        (root, last_commit)
        for (
            root,
            last_commit,
            commit,
            has_mirror_in_s3,
        ) in last_root_commits_in_s3
        if (
            commit is not None
            and commit == last_commit
            and has_mirror_in_s3
            and force is False
        )
    )
    await collect(
        [
            update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=root.cloning.status,
                message=root.cloning.reason,
                commit=last_commit,
            )
            for root, last_commit in unchanged_roots
        ]
    )

    valid_roots = tuple(
        root
        for (
            root,
            last_commit,
            commit,
            has_mirror_in_s3,
        ) in last_root_commits_in_s3
        if (
            commit is not None
            and (
                commit != last_commit or not has_mirror_in_s3 or force is True
            )
        )
        or (queue_with_vpn and root.state.use_vpn)
    )

    return valid_roots


async def queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    roots: tuple[GitRoot, ...] | None = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
    from_scheduler: bool = False,
) -> PutActionResult | None:
    group: Group = await loaders.group.load(group_name)
    if roots is None:
        roots = tuple(
            root
            for root in await loaders.group_roots.load(group_name)
            if (
                isinstance(root, GitRoot)
                and root.state.credential_id is not None
            )
        )
    valid_roots = _filter_active_roots_with_credentials(roots, queue_with_vpn)
    if not group.state.has_squad and not force:
        valid_roots = await _filter_roots_unsolved_events(
            valid_roots, loaders, group_name
        )

    if check_existing_jobs:
        valid_roots = await _filter_roots_already_in_queue(
            valid_roots, group_name
        )

    valid_roots = await _filter_roots_working_creds(
        valid_roots,
        loaders,
        group_name,
        group.organization_id,
        force,
        queue_with_vpn,
    )
    if valid_roots:
        additional_info = json.dumps(
            {
                "group_name": group_name,
                "roots": list({root.state.nickname for root in valid_roots}),
            }
        )
        result_clone = await put_action(
            action=Action.CLONE_ROOTS,
            attempt_duration_seconds=5400,
            vcpus=1,
            memory=1800,
            entity=group_name,
            subject=user_email,
            additional_info=additional_info,
            queue=IntegratesBatchQueue.CLONE,
            product_name=Product.INTEGRATES,
            dynamodb_pk=None,
        )
        if result_clone.batch_job_id:
            result_refresh = await put_action(
                action=Action.REFRESH_TOE_LINES,
                additional_info="*",
                attempt_duration_seconds=7200,
                entity=group_name,
                product_name=Product.INTEGRATES,
                subject="integrates@fluidattacks.com",
                queue=IntegratesBatchQueue.SMALL,
                dependsOn=[
                    {
                        "jobId": result_clone.batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )
            if result_refresh.batch_job_id:
                await put_action(
                    action=Action.REBASE,
                    additional_info=additional_info,
                    entity=group_name,
                    product_name=Product.INTEGRATES,
                    subject="integrates@fluidattacks.com",
                    queue=IntegratesBatchQueue.SMALL,
                    attempt_duration_seconds=14400,
                    dependsOn=[
                        {
                            "jobId": result_refresh.batch_job_id,
                            "type": "SEQUENTIAL",
                        },
                    ],
                )
        if not from_scheduler:
            await collect(
                tuple(
                    update_root_cloning_status(
                        loaders=loaders,
                        group_name=group_name,
                        root_id=root.id,
                        status=GitCloningStatus.QUEUED,
                        message="Cloning queued...",
                    )
                    for root in valid_roots
                )
            )

        return result_clone
    return None


async def get_commit_last_sucessful_clone(
    loaders: Dataloaders, root: GitRoot
) -> str | None:
    commit = root.cloning.commit
    if commit is None:
        clone_history: list[
            GitRootCloning
        ] = await loaders.root_historic_cloning.load(root.id)
        for clone_state in reversed(clone_history):
            if clone_state.status == GitCloningStatus.OK:
                commit = clone_state.commit
                break

    return commit
