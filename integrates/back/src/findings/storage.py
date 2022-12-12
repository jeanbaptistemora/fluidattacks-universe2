from s3 import (
    operations as s3_ops,
)


async def download_evidence(file_name: str, file_path: str) -> None:
    await s3_ops.download_file(
        f"evidences/{file_name}",
        file_path,
    )


async def remove_evidence(file_name: str) -> None:
    await s3_ops.remove_file(f"evidences/{file_name}")


async def save_evidence(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"evidences/{file_name}",
    )


async def search_evidence(file_name: str) -> list[str]:
    return await s3_ops.list_files(f"evidences/{file_name}")
