from aioextensions import (
    in_thread,
)
import asyncio
import base64
from context import (
    SERVICES_GITLAB_API_TOKEN,
    SERVICES_GITLAB_API_USER,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidParameter,
)
from datetime import (
    datetime,
)
from git.exc import (
    GitCommandError,
)
from git.repo import (
    Repo,
)
import logging
from more_itertools import (
    pairwise,
)
from newutils import (
    datetime as datetime_utils,
)
import os
from settings.logger import (
    LOGGING,
)
import tempfile
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)
from unidiff import (
    Hunk,
    PatchedFile,
    PatchSet,
)
from urllib.parse import (
    quote,
    quote_plus,
    urlparse,
)
import uuid

logging.config.dictConfig(LOGGING)

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


def get_diff(
    repo: Repo,
    *,
    rev_a: str,
    rev_b: str,
    path: Optional[str] = None,
) -> Optional[PatchSet]:
    with suppress(GitCommandError):
        return PatchSet(
            repo.git.diff(
                "--color=never",
                "--minimal",
                "--patch",
                "--unified=0",
                f"{rev_a}...{rev_b}",
                "--",
                *((path,) if path else tuple()),
            ),
        )

    return None


def _rebase_one_commit_at_a_time(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    hunk: Hunk
    patch: PatchedFile

    diff = get_diff(repo, rev_a=rev_a, rev_b=rev_b, path=path)
    if diff is None:
        return None

    rebased_line = line
    for patch in diff:
        if patch.source_file == f"a/{path}":
            if patch.is_removed_file:
                # We cannot rebase something that was deleted
                return None
            # The original file matches the path to rebase
            # If the file was moved or something, this updates the path
            path = patch.target_file[2:]

            # Let's process the hunks to see what should be done with
            # the line numbers
            for hunk in patch:
                hunk_source_end = hunk.source_start + hunk.source_length - 1

                if line < hunk.source_start:
                    # The line exists before the hunk and therefore
                    # we do not need to modify the line
                    pass
                elif line > hunk_source_end:
                    # The line exists after this hunk and therefore
                    # we should increase/decrease the line number
                    rebased_line += hunk.added - hunk.removed
                elif hunk.source_start <= line <= hunk_source_end:
                    # We cannot rebase because the line was modified
                    # by this hunk
                    # We cannot guess the next position of the line
                    # deterministically
                    return None
    return RebaseResult(path=path, line=rebased_line, rev=rev_b)


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    rev: str = rev_a
    revs_str: str = repo.git.log(
        "--format=%H",
        "--reverse",
        f"{rev_a}...{rev_b}",
        path,
    )
    revs: list[str] = [rev_a] + revs_str.splitlines()

    # Let's rebase one commit at a time,
    # this way we reduce the probability of conflicts
    # and ensure line numbers are updated up to the latest possible commit
    for rev_1, rev_2 in pairwise(revs):
        if rebase_result := _rebase_one_commit_at_a_time(
            repo, path=path, line=line, rev_a=rev_1, rev_b=rev_2
        ):
            path = rebase_result.path
            line = rebase_result.line
            rev = rebase_result.rev
        else:
            # We cannot continue rebasing
            break

    if rev == rev_a:
        # We did not rebase anything
        return None

    return RebaseResult(path=path, line=line, rev=rev)
