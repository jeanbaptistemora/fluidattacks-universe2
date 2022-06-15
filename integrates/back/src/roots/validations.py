from custom_exceptions import (
    CredentialAlreadyExists,
    CredentialCanNotBeUsedInGroup,
    InactiveRoot,
    InvalidChar,
    InvalidGitCredentials,
    InvalidGitRoot,
    InvalidRootComponent,
    InvalidUrl,
    RepeatedRootNickname,
)
from db_model.credentials.types import (
    Credential,
    CredentialItem,
)
from db_model.enums import (
    CredentialType,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from git import (
    Git,
    GitCommandError,
)
from ipaddress import (
    ip_address,
)
import newutils.git
import os
import re
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)
from urllib.parse import (
    ParseResult,
    unquote_plus,
    urlparse,
)


async def validate_credential_name_in_organization(
    loaders: Any,
    new_credential: Credential,
) -> None:
    org_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(
        new_credential.organization_id
    )
    credential_names = {
        credential.state.name for credential in org_credentials
    }
    if new_credential.state.name in credential_names:
        raise CredentialAlreadyExists()


async def validate_credential_in_group_or_user(
    loaders: Any,
    credential_id: str,
    group_name: str,
    user_email: str,
) -> None:
    group_roots: tuple[Root, ...] = await loaders.group_roots.load(group_name)
    group_credential_ids = {
        root.state.credential_id
        for root in group_roots
        if isinstance(root, GitRoot) and root.state.credential_id
    }
    user_credentials: tuple[
        Credential, ...
    ] = await loaders.user_credentials_new.load(user_email)
    user_credential_ids = {credential.id for credential in user_credentials}
    allowed_credential_ids = group_credential_ids | user_credential_ids
    if credential_id not in allowed_credential_ids:
        raise CredentialCanNotBeUsedInGroup()


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
    url_attributes: ParseResult = urlparse(url)

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


def is_git_unique(url: str, branch: str, roots: Tuple[Root, ...]) -> bool:
    return (url, branch) not in tuple(
        (root.state.url, root.state.branch)
        for root in roots
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    )


def is_valid_ip(address: str) -> bool:
    try:
        ip_address(address)
        return True
    except ValueError:
        return False


def is_ip_unique(address: str, port: str, roots: Tuple[Root, ...]) -> bool:
    return (address, port) not in tuple(
        (root.state.address, root.state.port)
        for root in roots
        if isinstance(root, IPRoot) and root.state.status == RootStatus.ACTIVE
    )


def is_url_unique(  # pylint: disable=too-many-arguments
    host: str,
    path: str,
    port: str,
    protocol: str,
    query: Optional[str],
    roots: Tuple[Root, ...],
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
        if isinstance(root, URLRoot) and root.state.status == RootStatus.ACTIVE
    )


def validate_active_root(root: Root) -> None:
    if root.state.status == RootStatus.ACTIVE:
        return
    raise InactiveRoot()


def validate_credential_name(
    new_credential: CredentialItem,
    current_credentials: Tuple[CredentialItem, ...],
) -> None:
    credential_names = {
        credential.state.name for credential in current_credentials
    }
    if new_credential.state.name in credential_names:
        raise CredentialAlreadyExists()


async def validate_git_root_component(
    loaders: Any, root: Root, component: str
) -> None:
    if isinstance(root, GitRoot):
        env_urls: list[
            GitEnvironmentUrl
        ] = await loaders.git_environment_urls.load(root.id)
        env_urls = [*env_urls, *root.state.git_environment_urls]
        if component not in [x.url for x in env_urls] and not is_valid_url(
            component
        ):
            raise InvalidUrl()

        for environment_url in env_urls:
            formatted_environment_url = (
                environment_url.url
                if environment_url.url.endswith("/")
                else f"{environment_url.url}/"
            )
            if component == environment_url.url or component.startswith(
                formatted_environment_url
            ):
                return
        raise InvalidRootComponent()


def validate_url_root_component(root: Root, component: str) -> None:
    if isinstance(root, URLRoot):
        if not is_valid_url(component):
            raise InvalidUrl()
        url_with_port = (
            f"{root.state.host}:{root.state.port}"
            if root.state.port
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


def validate_ip_root_component(root: Root, component: str) -> None:
    if isinstance(root, IPRoot):
        host = (
            f"{root.state.address}:{root.state.port}"
            if root.state.port
            else root.state.address
        )
        if component == host or component.startswith(f"{host}/"):
            return
        raise InvalidRootComponent()


async def validate_component(loaders: Any, root: Root, component: str) -> None:
    await validate_git_root_component(loaders, root, component)
    validate_url_root_component(root, component)
    validate_ip_root_component(root, component)


def validate_git_root(root: Root) -> None:
    if not isinstance(root, GitRoot):
        raise InvalidGitRoot()


def validate_nickname(nickname: str) -> None:
    if not re.match(r"^[a-zA-Z_0-9-]{1,128}$", nickname):
        raise InvalidChar()


async def _validate_git_credentials_ssh(
    repo_url: str, credential_key: str
) -> None:
    las_commit = await newutils.git.ssh_ls_remote(
        repo_url=repo_url, credential_key=credential_key
    )
    if las_commit is None:
        raise InvalidGitCredentials()


async def _validate_git_credentials_https(
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
) -> None:
    las_commit = await newutils.git.https_ls_remote(
        repo_url=repo_url,
        password=password,
        token=token,
        user=user,
    )
    if las_commit is None:
        raise InvalidGitCredentials()


async def validate_git_credentials(
    repo_url: str, credential_type: CredentialType, credentials: Dict[str, str]
) -> None:
    if (credential_type.value == "SSH") and (
        credential_key := credentials.get("key")
    ):
        await _validate_git_credentials_ssh(repo_url, credential_key)
    elif credential_type.value == "HTTPS":
        await _validate_git_credentials_https(
            repo_url,
            token=credentials.get("token"),
            user=credentials.get("user"),
            password=credentials.get("password"),
        )
