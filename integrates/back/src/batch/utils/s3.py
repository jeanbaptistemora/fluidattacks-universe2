import aioboto3
import asyncio
from context import (
    FI_AWS_S3_MIRRORS_BUCKET,
    FI_ENVIRONMENT,
)
import json
import logging
from newutils import (
    datetime as datetime_utils,
)
import os
from s3.operations import (
    OPTIONS,
)
from settings.logger import (
    LOGGING,
)
import tempfile
from typing import (
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")


async def upload_cloned_repo_to_s3(
    *,
    repo_path: str,
    group_name: str,
    nickname: str,
) -> bool:
    success: bool = False

    # Add metadata about the last cloning date, which is right now
    with open(
        os.path.join(repo_path, ".git/fluidattacks_metadata"),
        "w",
        encoding="utf-8",
    ) as metadata:
        json.dump(
            {
                "date": datetime_utils.convert_to_iso_str(
                    datetime_utils.get_now_as_str()
                )
            },
            metadata,
            indent=2,
        )

    # Create .keep files in empty directories so the structure is kept in S3
    empty_dirs = [
        root
        for root, dirs, files in os.walk(repo_path)
        if not dirs and not files
    ]
    for _dir in empty_dirs:
        with open(os.path.join(_dir, ".keep"), "w", encoding="utf-8") as file:
            file.close()

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "sync",
        *(
            ("--endpoint-url", OPTIONS["endpoint_url"])
            if "endpoint_url" in OPTIONS
            else ()
        ),
        "--delete",
        *(() if FI_ENVIRONMENT == "development" else ("--sse", "AES256")),
        "--exclude",
        f"{repo_path}/*",
        "--include",
        f"{repo_path}/.git/*",
        repo_path,
        f"s3://{FI_AWS_S3_MIRRORS_BUCKET}/{group_name}/{nickname}/",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={**os.environ.copy()},
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error(
            "Uploading root to S3 failed with error: %s",
            stderr.decode(),
            extra=dict(extra=locals()),
        )
    else:
        success = True
    return success


async def upload_cloned_repo_to_s3_tar(
    *, repo_path: str, group_name: str, nickname: str
) -> bool:
    success: bool = False

    _, zip_output_path = tempfile.mkstemp()
    proc = await asyncio.create_subprocess_exec(
        "tar",
        "czf",
        zip_output_path,
        "--transform",
        f"flags=r;s/./{nickname}/",
        ".",
        cwd=repo_path,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error(
            "Failed to compress root \n stdout: %s\n stderr: %s",
            stdout.decode() if stdout else "",
            stderr.decode() if stderr else "",
            extra=dict(extra=locals()),
        )
        os.remove(zip_output_path)
        return False

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "cp",
        *(
            ("--endpoint-url", OPTIONS["endpoint_url"])
            if "endpoint_url" in OPTIONS
            else ()
        ),
        *(() if FI_ENVIRONMENT == "development" else ("--sse", "AES256")),
        zip_output_path,
        f"s3://{FI_AWS_S3_MIRRORS_BUCKET}/{group_name}/{nickname}.tar.gz",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={**os.environ.copy()},
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error(
            "Uploading root to S3 failed with error: %s",
            stderr.decode(),
            extra=dict(extra=locals()),
        )
    else:
        success = True
    os.remove(zip_output_path)
    return success


async def is_in_s3(group_name: str, root_nickname: str) -> Tuple[str, bool]:
    async with aioboto3.client(service_name="s3") as client:
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
