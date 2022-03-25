import aioboto3
import aiohttp
from db_model.roots.get import (
    get_upload_url_post,
)
import logging
import os
from settings.logger import (
    LOGGING,
)
import tarfile
import tempfile
from typing import (
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")
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
            ) as response:
                if response.status not in {200, 204}:
                    LOGGER.error(
                        "Uploading root to S3 failed with error %s",
                        await response.text(),
                        extra=dict(extra=locals()),
                    )
                else:
                    success = True

    os.remove(zip_output_path)
    return success


async def is_in_s3(group_name: str, root_nickname: str) -> Tuple[str, bool]:
    async with SESSION.client(service_name="s3") as client:
        return (
            root_nickname,
            any(
                object["Key"].startswith(f"{group_name}/{root_nickname}/.git/")
                for object in (
                    await client.list_objects(
                        Bucket="continuous-repositories",
                        Prefix=f"{group_name}/{root_nickname}/",
                    )
                ).get("Contents", [])
            ),
        )
