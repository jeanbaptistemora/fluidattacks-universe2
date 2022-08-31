import aioboto3
import aiohttp
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
import logging
from newutils.files import (
    iter_rel_paths,
    match_file,
)
import os
import pathspec
from settings.logger import (
    LOGGING,
)
import shutil
import tarfile
import tempfile
from typing import (
    Optional,
)
from urllib.request import (
    urlretrieve,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
SESSION = aioboto3.Session()


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: Optional[str] = None
) -> bool:
    git_dir = os.path.normpath(f"{repo_path}/.git")
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if os.path.exists(git_dir):
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

    response = await get_upload_url_post(group_name, nickname)
    object_name = f"{group_name}/{nickname}.tar.gz"
    with open(zip_output_path, "rb") as object_file:
        data = aiohttp.FormData()
        for key, value in response["fields"].items():
            data.add_field(key, value)
        data.add_field("file", object_file, filename=object_name)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                response["url"],
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
    # Get the expected repo name from the URL
    spec_ignore = pathspec.PathSpec.from_lines("gitwildmatch", git_ignore)
    # Compute what files should be deleted according to the scope rules
    for path in iter_rel_paths(repo_path):
        if match_file(spec_ignore.patterns, path):
            if path.startswith(".git/"):
                continue
            path_to_delete = os.path.join(repo_path, path)
            if os.path.isfile(path_to_delete):
                os.unlink(path_to_delete)
            elif os.path.isdir(path_to_delete):
                shutil.rmtree(path_to_delete)
    return True


async def download_repo(
    group_name: str,
    git_root: GitRoot,
    path_to_extract: str,
) -> None:
    download_url = await get_download_url(group_name, git_root.state.nickname)
    if not download_url:
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = f"{tmpdir}/{git_root.state.nickname}.tar.gz"
        urlretrieve(download_url, tar_path)  # nosec
        with tarfile.open(tar_path, "r:gz") as tar_handler:
            tar_handler.extractall(path_to_extract, numeric_owner=True)
            _delete_out_of_scope_files(
                git_root.state.gitignore, f"{tmpdir}/{git_root.state.nickname}"
            )
