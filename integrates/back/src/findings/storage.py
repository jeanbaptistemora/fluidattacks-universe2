from context import (
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from s3 import (
    operations as s3_ops,
)


async def download_evidence(file_name: str, file_path: str) -> None:
    await s3_ops.download_file(
        FI_AWS_S3_MAIN_BUCKET,
        f"{FI_AWS_S3_PATH_PREFIX}evidences/{file_name}",
        file_path,
    )


async def remove_evidence(file_name: str) -> None:
    await s3_ops.remove_file(
        FI_AWS_S3_MAIN_BUCKET, f"{FI_AWS_S3_PATH_PREFIX}evidences/{file_name}"
    )


async def save_evidence(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_MAIN_BUCKET,
        file_object,
        f"{FI_AWS_S3_PATH_PREFIX}evidences/{file_name}",
    )


async def search_evidence(file_name: str) -> list[str]:
    return await s3_ops.list_files(
        FI_AWS_S3_MAIN_BUCKET, f"{FI_AWS_S3_PATH_PREFIX}evidences/{file_name}"
    )
