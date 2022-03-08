from aioextensions import (
    in_thread,
)
import asyncio
import base64
from context import (
    SERVICES_GITLAB_API_TOKEN,
    SERVICES_GITLAB_API_USER,
)
from custom_exceptions import (
    InvalidParameter,
)
from datetime import (
    datetime,
)
from git import (
    Repo,
)
from newutils import (
    datetime as datetime_utils,
)
import os
import tempfile
from typing import (
    NamedTuple,
    Optional,
)
from urllib.parse import (
    urlparse,
)
import uuid


class CommitInfo(NamedTuple):
    hash: str
    author: str
    modified_date: datetime


def clone_services_repository(path: str) -> None:
    """Clone the services repository into a local directory"""
    repo_url = (
        f"https://{SERVICES_GITLAB_API_USER}:{SERVICES_GITLAB_API_TOKEN}"
        "@gitlab.com/fluidattacks/services.git"
    )
    Repo.clone_from(
        repo_url,
        path,
        multi_options=[
            "--depth=1",
        ],
    )


async def disable_quotepath(git_path: str) -> None:
    await asyncio.create_subprocess_exec(
        "git",
        f"--git-dir={git_path}",
        "config",
        "core.quotepath",
        "off",
    )


async def get_last_commit_author(repo: Repo, filename: str) -> str:
    """Get the last commiter's email of a file"""
    return str(
        await in_thread(
            repo.git.log, "--max-count", "1", "--format=%ce", "--", filename
        )
    )


async def get_last_commit_info(repo: Repo, filename: str) -> CommitInfo:
    """Get last hash of a file in the repo"""
    git_log = str(
        await in_thread(
            repo.git.log,
            "--max-count",
            "1",
            "--format=%H%n%ce%n%cI",
            "--",
            filename,
        )
    ).splitlines()
    return CommitInfo(
        hash=git_log[0],
        author=git_log[1],
        modified_date=datetime.fromisoformat(git_log[2]),
    )


async def get_last_commit_hash(repo: Repo, filename: str) -> str:
    """Get last hash of a file in the repo"""
    return str(
        await in_thread(
            repo.git.log, "--max-count", "1", "--format=%H", "--", filename
        )
    )


async def get_last_modified_date(repo: Repo, filename: str) -> str:
    """Get last modified date of a file in the repo"""
    return datetime_utils.get_as_utc_iso_format(
        datetime.fromisoformat(
            await in_thread(
                repo.git.log,
                "--max-count",
                "1",
                "--format=%cI",
                "--",
                filename,
            )
        )
    )


async def ssh_ls_remote(
    repo_url: str,
    credential_key: str,
    branch: str = "HEAD",
) -> Optional[str]:
    parsed_url = urlparse(repo_url)
    raw_root_url = repo_url.replace(f"{parsed_url.scheme}://", "")

    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(credential_key).decode())

        proc = await asyncio.create_subprocess_exec(
            "git",
            "ls-remote",
            raw_root_url,
            branch,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name} -o"
                    "UserKnownHostsFile=/dev/null -o "
                    "StrictHostKeyChecking=no"
                ),
            },
        )
        stdout, _ = await proc.communicate()

        os.remove(ssh_file_name)

        if proc.returncode != 0:
            return None

        return stdout.decode().split("\t")[0]


async def https_ls_remote(
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    branch: str = "HEAD",
) -> Optional[str]:
    parsed_url = urlparse(repo_url)
    if token is not None:
        url = repo_url.replace(
            parsed_url.netloc, f"{token}@{parsed_url.netloc}"
        )
    elif user is not None and password is not None:
        url = repo_url.replace(
            parsed_url.netloc, f"{user}:{password}@{parsed_url.netloc}"
        )
    else:
        raise InvalidParameter()

    proc = await asyncio.create_subprocess_exec(
        "git",
        "ls-remote",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, _ = await proc.communicate()

    if proc.returncode != 0:
        return None

    return stdout.decode().split("\t")[0]
