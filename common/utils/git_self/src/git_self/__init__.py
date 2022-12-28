import asyncio
import base64
from datetime import (
    datetime,
    timezone,
)
from git.exc import (
    GitCommandError,
)
from git.repo import (
    Repo,
)
import logging
import os
import tempfile
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)
from urllib.parse import (
    quote,
    quote_plus,
    urlparse,
)
import uuid

# Constants
LOGGER = logging.getLogger(__name__)


class CommitInfo(NamedTuple):
    hash: str
    author: str
    modified_date: datetime


class RebaseResult(NamedTuple):
    path: str
    line: int
    rev: str


class InvalidParameter(Exception):
    """Exception to control empty required parameters"""

    def __init__(self, field: str = "") -> None:
        """Constructor"""
        if field:
            msg = f"Exception - Field {field} is invalid"
        else:
            msg = "Exception - Error value is not valid"
        super().__init__(msg)


def _get_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


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
        repo.git.log("--max-count", "1", "--format=%ce", "--", filename)
    )


async def get_last_commit_info(repo: Repo, filename: str) -> CommitInfo:
    """Get last hash of a file in the repo"""
    git_log = str(
        repo.git.log(
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
    return str(repo.git.log("--max-count", "1", "--format=%H", "--", filename))


async def get_last_modified_date(repo: Repo, filename: str) -> str:
    """Get last modified date of a file in the repo"""
    return _get_as_utc_iso_format(
        datetime.fromisoformat(
            repo.git.log(
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
    raw_root_url = repo_url
    if "source.developers.google" not in raw_root_url:
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
                    f"ssh -i {ssh_file_name}"
                    " -o UserKnownHostsFile=/dev/null"
                    " -o StrictHostKeyChecking=no"
                    " -o IdentitiesOnly=yes"
                    " -o HostkeyAlgorithms=+ssh-rsa"
                    " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
                ),
            },
        )
        stdout, stderr = await proc.communicate()

        if stderr and proc.returncode != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra=dict(
                    extra={
                        "error": stderr.decode(),
                        "repo_url": repo_url,
                    }
                ),
            )

        os.remove(ssh_file_name)

        if proc.returncode != 0:
            return None

        return stdout.decode().split("\t")[0]


def _format_https_url(
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    user = quote_plus(user) if user is not None else user
    password = quote_plus(password) if password is not None else password

    parsed_url = urlparse(repo_url)
    parsed_url = parsed_url._replace(path=quote(parsed_url.path))
    host = parsed_url.netloc
    if "@" in host:
        host = host.split("@")[-1]

    if token is not None:
        url = (parsed_url._replace(netloc=f"{token}@{host}")).geturl()
    elif user is not None and password is not None:
        url = (
            parsed_url._replace(netloc=f"{user}:{password}@{host}")
        ).geturl()
    else:
        raise InvalidParameter()

    return url


async def https_ls_remote(
    repo_url: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    branch: str = "HEAD",
) -> Optional[str]:
    url = _format_https_url(repo_url, user, password, token)

    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        "ls-remote",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, _stderr = await asyncio.wait_for(proc.communicate(), 20)
        if _stderr and proc.returncode != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra=dict(
                    extra={
                        "error": _stderr.decode(),
                        "repo_url": repo_url,
                    }
                ),
            )
    except asyncio.exceptions.TimeoutError:
        LOGGER.warning(
            "git remote-ls time out",
            extra={"extra": {"repo_url": repo_url}},
        )
        return None

    if proc.returncode != 0:
        return None

    return stdout.decode().split("\t")[0]


async def ssh_clone(
    *, branch: str, credential_key: str, repo_url: str, temp_dir: str
) -> Tuple[Optional[str], Optional[str]]:
    raw_root_url = repo_url
    if "source.developers.google" not in raw_root_url:
        raw_root_url = repo_url.replace(f"{urlparse(repo_url).scheme}://", "")
    ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
    with open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        ssh_file.write(base64.b64decode(credential_key).decode())

    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        raw_root_url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={
            **os.environ.copy(),
            "GIT_SSH_COMMAND": (
                f"ssh -i {ssh_file_name}"
                " -o UserKnownHostsFile=/dev/null"
                " -o StrictHostKeyChecking=no"
                " -o IdentitiesOnly=yes"
                " -o HostkeyAlgorithms=+ssh-rsa"
                " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
            ),
        },
    )
    _, stderr = await proc.communicate()

    os.remove(ssh_file_name)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: Optional[str] = None,
    token: Optional[str] = None,
    user: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    url = _format_https_url(repo_url, user, password, token)
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        "clone",
        "--branch",
        branch,
        "--single-branch",
        url,
        folder_to_clone_root,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(
        "Repo cloning failed", extra={"extra": {"message": stderr.decode()}}
    )

    return (None, stderr.decode("utf-8"))


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    try:
        result: list[str] = repo.git.blame(
            f"{rev_a}..{rev_b}",
            "--",
            path,
            L=f"{line},+1",
            l=True,
            p=True,
            show_number=True,
            reverse=True,
            show_name=True,
        ).splitlines()
    except GitCommandError:
        return None

    new_rev = result[0].split(" ")[0]
    new_line = int(result[0].split(" ")[1])
    new_path = next(
        (row.split(" ")[1] for row in result if row.startswith("filename ")),
        path,
    )

    if new_rev == rev_a or (new_line == line and new_path == path):
        # We did not rebase anything
        return None

    return RebaseResult(path=new_path, line=new_line, rev=new_rev)


def make_group_dir(tmpdir: str, group_name: str) -> None:
    group_dir = os.path.join(tmpdir, "groups", group_name, "fusion")
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    make_group_dir(tmpdir, group_name)
    call_melts = [
        "CI=true",
        "CI_COMMIT_REF_NAME=trunk",
        f"melts drills --pull-repos {group_name}",
    ]
    if optional_repo_nickname:
        call_melts.append(f"--name {optional_repo_nickname}")
    os.system(" ".join(call_melts))  # nosec
    os.system(f"chmod -R +r {os.path.join(tmpdir, 'groups')}")  # nosec
