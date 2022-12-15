from custom_exceptions import (
    BranchNotFound,
    InactiveRoot,
    InvalidChar,
    InvalidGitCredentials,
    InvalidGitRoot,
    InvalidRootComponent,
    InvalidUrl,
    RepeatedRootNickname,
    RequiredCredentials,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    Root,
    RootEnvironmentUrl,
    URLRoot,
)
from git.cmd import (
    Git,
)
from git.exc import (
    GitCommandError,
)
from ipaddress import (
    ip_address,
)
import newutils.git_self
from organizations import (
    utils as orgs_utils,
)
import os
import re
from roots import (
    utils as roots_utils,
)
from typing import (
    Any,
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
    Url,
)
from urllib.parse import (
    ParseResult,
    unquote_plus,
    urlparse,
)


async def validate_git_access(
    url: str,
    branch: str,
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret],
) -> None:
    try:
        url = roots_utils.format_git_repo_url(url)
    except LocationParseError as ex:
        raise InvalidUrl() from ex

    if isinstance(secret, SshSecret):
        secret = SshSecret(
            key=orgs_utils.format_credentials_ssh_key(secret.key)
        )
    await validate_git_credentials(url, branch, secret)


async def validate_credential_in_organization(
    loaders: Any,
    credential_id: str,
    organization_id: str,
) -> None:
    await loaders.credentials.load(
        CredentialsRequest(
            id=credential_id,
            organization_id=organization_id,
        )
    )


async def working_credentials(
    url: str,
    branch: str,
    credentials: Optional[Credentials],
) -> None:
    if not credentials:
        raise RequiredCredentials()

    await validate_git_access(
        url=url, branch=branch, secret=credentials.state.secret
    )


def is_exclude_valid(exclude_patterns: List[str], url: str) -> bool:
    is_valid: bool = True

    # Get repository name
    url_obj = urlparse(url)
    url_path = unquote_plus(url_obj.path)
    repo_name = os.path.basename(url_path)
    if repo_name.endswith(".git"):
        repo_name = repo_name[0:-4]

    for pattern in exclude_patterns:
        pattern_as_list: List[str] = pattern.lower().split("/")
        if (
            repo_name in pattern_as_list
            and pattern_as_list.index(repo_name) == 0
        ):
            is_valid = False
    return is_valid


def is_valid_url(url: str) -> bool:
    try:
        url_attributes: Union[Url, ParseResult] = parse_url(url)
    except LocationParseError:
        url_attributes = urlparse(url)

    return bool(url_attributes.netloc and url_attributes.scheme)


def is_valid_git_branch(branch_name: str) -> bool:
    try:
        Git().check_ref_format("--branch", branch_name)
        return True
    except GitCommandError:
        return False


def validate_nickname_is_unique(
    nickname: str, roots: Tuple[Root, ...], old_nickname: str = ""
) -> None:
    if nickname != old_nickname and nickname in {
        root.state.nickname
        for root in roots
        if root.state.status == RootStatus.ACTIVE
    }:
        raise RepeatedRootNickname()


def is_git_unique(
    url: str,
    branch: str,
    group_name: str,
    roots: Tuple[Root, ...],
    include_inactive: bool = False,
) -> bool:
    """
    Validation util to check whether a git root is unique

    This logic must match the associated documentation page at:
    https://docs.fluidattacks.com/machine/web/groups/scope/roots#single-root-assessment
    """
    for root in roots:
        if (
            isinstance(root, GitRoot)
            and (root.state.status == RootStatus.ACTIVE or include_inactive)
            and root.state.reason != "GROUP_DELETED"
        ):
            if (url.lower(), group_name) == (
                root.state.url.lower(),
                root.group_name,
            ):
                return False

            if (url.lower(), branch) == (
                root.state.url.lower(),
                root.state.branch,
            ):
                return False

    return True


def is_valid_ip(address: str) -> bool:
    try:
        ip_address(address)
        return True
    except ValueError:
        return False


def is_ip_unique(
    address: str,
    roots: Tuple[Root, ...],
    include_inactive: bool = False,
) -> bool:
    return address not in tuple(
        root.state.address
        for root in roots
        if isinstance(root, IPRoot)
        and (root.state.status == RootStatus.ACTIVE or include_inactive)
        and root.state.reason != "GROUP_DELETED"
    )


def is_url_unique(  # pylint: disable=too-many-arguments
    host: str,
    path: str,
    port: str,
    protocol: str,
    query: Optional[str],
    roots: Tuple[Root, ...],
    include_inactive: bool = False,
) -> bool:
    return (host, path, port, protocol, query) not in tuple(
        (
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol,
            root.state.query,
        )
        for root in roots
        if isinstance(root, URLRoot)
        and (root.state.status == RootStatus.ACTIVE or include_inactive)
        and root.state.reason != "GROUP_DELETED"
    )


def validate_active_root(root: Root) -> None:
    if root.state.status == RootStatus.ACTIVE:
        return
    raise InactiveRoot()


def _validate_aws_component(
    component: str, env_urls: list[RootEnvironmentUrl]
) -> bool:
    return any(
        x.url in component
        for x in env_urls
        if x.cloud_name and x.cloud_name.value == "AWS"
    )


async def validate_git_root_component(
    loaders: Any, root: Root, component: str
) -> None:
    if not isinstance(root, GitRoot):
        return
    env_urls: list[
        RootEnvironmentUrl
    ] = await loaders.root_environment_urls.load(root.id)
    env_urls = [*env_urls, *root.state.git_environment_urls]
    if (
        component not in [x.url for x in env_urls]
        and not is_valid_url(component)
        and not any(component.startswith(x.url) for x in env_urls)
        and not _validate_aws_component(component, env_urls)
    ):
        raise InvalidUrl()

    for environment_url in env_urls:
        formatted_environment_url = (
            environment_url.url
            if environment_url.url.endswith("/")
            else f"{environment_url.url}/"
        )
        formatted_component = (
            component if component.endswith("/") else f"{component}/"
        )
        parsed_environment_url = parse_url(formatted_environment_url)
        parsed_component = parse_url(formatted_component)
        if (
            (  # pylint: disable=too-many-boolean-expressions
                formatted_component.startswith(formatted_environment_url)
            )
            or (
                parsed_component.scheme == parsed_environment_url.scheme
                and parsed_component.host == parsed_environment_url.host
                and parsed_component.port == parsed_environment_url.port
            )
            or (
                environment_url.cloud_name
                and environment_url.cloud_name.value == "AWS"
                and environment_url.url in component
            )
        ):

            return
    raise InvalidRootComponent()


def validate_url_root_component(root: Root, component: str) -> None:
    if isinstance(root, URLRoot):
        if not is_valid_url(component):
            raise InvalidUrl()
        url_with_port = (
            f"{root.state.host}:{root.state.port}"
            if root.state.port and root.state.protocol != "FILE"
            else root.state.host
        )

        if root.state.query is None and f"{component}/".startswith(
            f"{root.state.protocol.lower()}://{url_with_port}"
            f"{root.state.path.removesuffix('/')}/"
        ):
            return

        if (
            root.state.query is not None
            and component == f"{root.state.protocol.lower()}://{url_with_port}"
            f"{root.state.path}?{root.state.query}"
        ):
            return
        raise InvalidRootComponent()


async def validate_component(loaders: Any, root: Root, component: str) -> None:
    await validate_git_root_component(loaders, root, component)
    validate_url_root_component(root, component)


def validate_git_root(root: Root) -> None:
    if not isinstance(root, GitRoot):
        raise InvalidGitRoot()


def validate_nickname(nickname: str) -> None:
    if not re.match(r"^[a-zA-Z_0-9-]{1,128}$", nickname):
        raise InvalidChar()


async def _validate_git_credentials_ssh(
    repo_url: str, branch: str, credential_key: str
) -> None:
    last_commit = await newutils.git_self.ssh_ls_remote(
        repo_url=repo_url,
        branch=branch,
        credential_key=credential_key,
    )
    if last_commit is None:
        raise InvalidGitCredentials()

    if not last_commit:
        raise BranchNotFound()


async def _validate_git_credentials_https(
    repo_url: str,
    branch: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
) -> None:
    last_commit = await newutils.git_self.https_ls_remote(
        branch=branch,
        repo_url=repo_url,
        password=password,
        token=token,
        user=user,
    )
    if last_commit is None:
        raise InvalidGitCredentials()

    if not last_commit:
        raise BranchNotFound()


async def validate_git_credentials(
    repo_url: str,
    branch: str,
    secret: Union[HttpsSecret, HttpsPatSecret, SshSecret],
) -> None:
    if isinstance(secret, SshSecret):
        await _validate_git_credentials_ssh(repo_url, branch, secret.key)
    elif isinstance(secret, HttpsPatSecret):
        await _validate_git_credentials_https(
            repo_url,
            branch=branch,
            token=secret.token,
            user=None,
            password=None,
        )
    elif isinstance(secret, HttpsSecret):
        await _validate_git_credentials_https(
            repo_url,
            branch=branch,
            token=None,
            user=secret.user,
            password=secret.password,
        )
