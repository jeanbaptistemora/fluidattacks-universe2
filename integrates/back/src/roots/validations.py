import asyncio
import base64
from custom_exceptions import (
    InactiveRoot,
    InvalidChar,
    InvalidGitCredentials,
    InvalidRootComponent,
    RepeatedRootNickname,
)
from db_model.enums import (
    CredentialType,
)
from db_model.roots.types import (
    GitRootItem,
    IPRootItem,
    RootItem,
    URLRootItem,
)
from git import (
    Git,
    GitCommandError,
)
from ipaddress import (
    ip_address,
)
import os
import re
import tempfile
from typing import (
    List,
    Tuple,
)
from urllib.parse import (
    ParseResult,
    unquote_plus,
    urlparse,
)
import uuid


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
    nickname: str, roots: Tuple[RootItem, ...], old_nickname: str = ""
) -> None:
    if nickname != old_nickname and nickname in {
        root.state.nickname for root in roots if root.state.status == "ACTIVE"
    }:
        raise RepeatedRootNickname()


def is_git_unique(url: str, roots: Tuple[RootItem, ...]) -> bool:
    return url not in tuple(
        root.state.url
        for root in roots
        if isinstance(root, GitRootItem) and root.state.status == "ACTIVE"
    )


def is_valid_ip(address: str) -> bool:
    try:
        ip_address(address)
        return True
    except ValueError:
        return False


def is_ip_unique(address: str, port: str, roots: Tuple[RootItem, ...]) -> bool:
    return (address, port) not in tuple(
        (root.state.address, root.state.port)
        for root in roots
        if isinstance(root, IPRootItem) and root.state.status == "ACTIVE"
    )


def is_url_unique(
    host: str, path: str, port: str, protocol: str, roots: Tuple[RootItem, ...]
) -> bool:
    return (host, path, port, protocol) not in tuple(
        (
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol,
        )
        for root in roots
        if isinstance(root, URLRootItem) and root.state.status == "ACTIVE"
    )


def validate_active_root(root: RootItem) -> None:
    if root.state.status == "ACTIVE":
        return
    raise InactiveRoot()


def validate_component(root: RootItem, component: str) -> None:
    if isinstance(root, GitRootItem):
        for environment_url in root.state.environment_urls:
            if component == environment_url or component.startswith(
                f"{environment_url}/"
            ):
                return

    if isinstance(root, URLRootItem):
        host = (
            f"{root.state.host}:{root.state.port}"
            if root.state.port
            else root.state.host
        )
        if component.startswith(
            f"{root.state.protocol.lower()}://{host}{root.state.path}"
        ):
            return

    if isinstance(root, IPRootItem):
        host = (
            f"{root.state.address}:{root.state.port}"
            if root.state.port
            else root.state.address
        )
        if component == host or component.startswith(f"{host}/"):
            return

    raise InvalidRootComponent()


def validate_nickname(nickname: str) -> None:
    if not re.match(r"^[a-zA-Z_0-9-]{1,128}$", nickname):
        raise InvalidChar()


async def validate_git_credentials(
    repo_url: str, credential_type: CredentialType, credential_key: str
) -> None:
    if credential_type == "SSH":
        with tempfile.TemporaryDirectory() as temp_dir:
            ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
            parsed_url = urlparse(repo_url)
            url = repo_url.replace(f"{parsed_url.scheme}://", "")
            with open(
                os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
                "w",
                encoding="utf-8",
            ) as ssh_file:
                ssh_file.write(base64.b64decode(credential_key).decode())

            proc = await asyncio.create_subprocess_exec(
                "git",
                "ls-remote",
                "-h",
                url,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                env={
                    **os.environ.copy(),
                    "GIT_SSH_COMMAND": f"ssh -i {ssh_file_name}",
                },
            )
            await proc.communicate()
            if proc.returncode != 0:
                raise InvalidGitCredentials()
