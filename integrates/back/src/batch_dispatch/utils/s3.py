import aioboto3
import aiohttp
from contextlib import (
    suppress,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
)
from db_model.roots.get import (
    get_download_url,
    get_upload_url_post,
)
from db_model.roots.types import (
    GitRoot,
)
from git import (
    GitError,
    InvalidGitRepositoryError,
)
from git.cmd import (
    Git,
)
from git.repo.base import (
    Repo,
)
import logging
from newutils.files import (
    iter_rel_paths,
    match_files,
)
import os
from os import (
    path,
)
from settings.logger import (
    LOGGING,
)
import shutil
import tarfile
import tempfile
from urllib.request import (
    urlretrieve,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
SESSION = aioboto3.Session()


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: str | None = None
) -> bool:
    git_dir = path.normpath(f"{repo_path}/.git")
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if path.exists(git_dir):
            tar_handler.add(
                git_dir, arcname=f"{root_nickname}/.git", recursive=True
            )
            return True
        return False


async def upload_cloned_repo_to_s3_tar(
    *, repo_path: str, group_name: str, nickname: str
) -> bool:
    success: bool = False

    _, zip_output_path = tempfile.mkstemp()
    create_git_root_tar_file(nickname, repo_path, zip_output_path)

    if not create_git_root_tar_file(nickname, repo_path, zip_output_path):
        LOGGER.error(
            "Failed to compress root %s",
            nickname,
            extra=dict(extra=locals()),
        )
        os.remove(zip_output_path)
        return False

    url, fields = await get_upload_url_post(group_name, nickname)
    object_name = path.join(group_name, f"{nickname}.tar.gz")
    with open(zip_output_path, "rb") as object_file:
        data = aiohttp.FormData()
        for key, value in fields.items():
            data.add_field(key, value)
        data.add_field("file", object_file, filename=object_name)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data=data,
            ) as upload_response:
                if upload_response.status not in {200, 204}:
                    LOGGER.error(
                        "Uploading root to S3 failed with error %s",
                        await upload_response.text(),
                        extra=dict(extra=locals()),
                    )
                    raise ErrorUploadingFileS3()
                success = True

    os.remove(zip_output_path)
    return success


def _delete_out_of_scope_files(git_ignore: list[str], repo_path: str) -> bool:
    # Compute what files should be deleted according to the scope rules
    for file_path in match_files(git_ignore, iter_rel_paths(repo_path)):
        if file_path.startswith(".git/"):
            continue
        path_to_delete = path.join(repo_path, file_path)
        if os.path.isfile(path_to_delete):
            with suppress(FileNotFoundError):
                os.unlink(path_to_delete)
        elif os.path.isdir(path_to_delete):
            shutil.rmtree(path_to_delete, ignore_errors=True)

    return True


async def download_repo(
    group_name: str,
    git_root: GitRoot,
    path_to_extract: str,
) -> bool:
    download_url = await get_download_url(group_name, git_root.state.nickname)
    if not download_url:
        LOGGER.warning(
            "can not find download url",
            extra={
                "extra": {
                    "group_name": group_name,
                    "repository": git_root.state.nickname,
                }
            },
        )
        return False
    repo_path = path.join(path_to_extract, git_root.state.nickname)
    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = path.join(tmpdir, f"{git_root.state.nickname}.tar.gz")
        urlretrieve(download_url, tar_path)  # nosec
        with tarfile.open(tar_path, "r:gz") as tar_handler:
            tar_handler.extractall(path_to_extract, numeric_owner=True)
        if not path.exists(repo_path):
            LOGGER.error(
                "No such repository path",
                extra={
                    "extra": {
                        "group_name": group_name,
                        "repository": git_root.state.nickname,
                    }
                },
            )
            return False

        with suppress(GitError):
            Git().execute(
                [
                    "git",
                    "config",
                    "--global",
                    "--add",
                    "safe.directory",
                    repo_path,
                ]
            )
        try:
            repo = Repo(repo_path)
        except InvalidGitRepositoryError:
            LOGGER.error(
                "Invalid repository",
                extra={
                    "extra": {
                        "group_name": group_name,
                        "repository": git_root.state.nickname,
                    }
                },
            )
            return False

        try:
            repo.git.reset("--hard", "HEAD")
        except GitError as exc:
            LOGGER.error(
                "Error expanding repository",
                extra={
                    "extra": {
                        "exception": str(exc),
                        "group_name": git_root.group_name,
                        "root_id": git_root.id,
                        "root_nickname": git_root.state.nickname,
                    }
                },
            )
            return False

        try:
            repo_branch = getattr(repo.heads, git_root.state.branch)
            repo_branch.checkout()
        except AttributeError:
            LOGGER.error(
                "Branch not found",
                extra={
                    "extra": {
                        "branch": git_root.state.branch,
                        "group_name": group_name,
                        "repository": git_root.state.nickname,
                    }
                },
            )
            return False
        _delete_out_of_scope_files(
            git_root.state.gitignore,
            path.join(path_to_extract, git_root.state.nickname),
        )
        return True
