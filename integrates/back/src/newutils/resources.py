from context import (
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from s3 import (
    operations as s3_ops,
)
from typing import (
    Dict,
)


async def download_file(file_info: str, group_name: str) -> str:
    group_name = group_name.lower()
    file_url = f"{FI_AWS_S3_PATH_PREFIX}resources/{group_name}/{file_info}"
    return await s3_ops.sign_url(
        file_url,
        10,
        FI_AWS_S3_MAIN_BUCKET,
    )


async def upload_file(
    file_info: str, group_name: str
) -> Dict[str, Dict[str, str]]:
    group_name = group_name.lower()
    file_url = f"{FI_AWS_S3_PATH_PREFIX}resources/{group_name}/{file_info}"
    return await s3_ops.sing_upload_url(
        file_url,
        10,
        FI_AWS_S3_MAIN_BUCKET,
    )


async def remove_file(file_name: str) -> None:
    await s3_ops.remove_file(
        FI_AWS_S3_MAIN_BUCKET,
        f"{FI_AWS_S3_PATH_PREFIX}resources/{file_name}",
    )


async def save_file(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_MAIN_BUCKET,
        file_object,
        f"{FI_AWS_S3_PATH_PREFIX}resources/{file_name}",
    )


async def search_file(file_name: str) -> list[str]:
    return await s3_ops.list_files(
        FI_AWS_S3_MAIN_BUCKET,
        f"{FI_AWS_S3_PATH_PREFIX}resources/{file_name}",
    )
