from newutils import (
    validations,
)
from s3 import (
    operations as s3_ops,
)


async def download_file(file_info: str, group_name: str) -> str:
    group_name = group_name.lower()
    file_url = f"resources/{group_name}/{file_info}"
    return await s3_ops.sign_url(
        file_url,
        10,
    )


@validations.validate_file_name_deco("file_info")
async def upload_file(
    file_info: str, group_name: str
) -> dict[str, dict[str, str]]:
    group_name = group_name.lower()
    file_url = f"resources/{group_name}/{file_info}"
    return await s3_ops.sing_upload_url(
        file_url,
        10,
    )


async def remove_file(file_name: str) -> None:
    await s3_ops.remove_file(
        f"resources/{file_name}",
    )


async def save_file(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"resources/{file_name}",
    )


async def search_file(file_name: str) -> list[str]:
    return await s3_ops.list_files(
        f"resources/{file_name}",
    )
