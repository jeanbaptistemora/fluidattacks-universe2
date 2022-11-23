from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from s3 import (
    operations as s3_ops,
)
from typing import (
    List,
)


async def download_evidence(file_name: str, file_path: str) -> None:
    await s3_ops.download_file(
        FI_AWS_S3_MAIN_BUCKET, f"evidences/{file_name}", file_path
    )


async def remove_evidence(file_name: str) -> None:
    await s3_ops.remove_file(FI_AWS_S3_MAIN_BUCKET, f"evidences/{file_name}")


async def save_evidence(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_MAIN_BUCKET,
        file_object,
        f"evidences/{file_name}",
    )


async def search_evidence(file_name: str) -> List[str]:
    return await s3_ops.list_files(
        FI_AWS_S3_MAIN_BUCKET, f"evidences/{file_name}"
    )
