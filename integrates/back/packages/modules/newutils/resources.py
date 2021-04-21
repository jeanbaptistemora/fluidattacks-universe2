# Standard libraries
from typing import List

# Third-party libraries

# Local libraries
from s3 import operations as s3_ops
from __init__ import FI_AWS_S3_RESOURCES_BUCKET


async def download_file(file_info: str, group_name: str) -> str:
    group_name = group_name.lower()
    file_url = f'{group_name}/{file_info}'
    return await s3_ops.sign_url(file_url, 10, FI_AWS_S3_RESOURCES_BUCKET)


async def remove_file(file_name: str) -> bool:
    return await s3_ops.remove_file(FI_AWS_S3_RESOURCES_BUCKET, file_name)


async def save_file(file_object: object, file_name: str) -> bool:
    return await s3_ops.upload_memory_file(
        FI_AWS_S3_RESOURCES_BUCKET,
        file_object,
        file_name
    )


async def search_file(file_name: str) -> List[str]:
    return await s3_ops.list_files(FI_AWS_S3_RESOURCES_BUCKET, file_name)
