from billing.domain import (
    remove_file,
    save_file,
    search_file,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
import os
import pytest
from s3.operations import (
    list_files,
)
from starlette.datastructures import (
    UploadFile,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_save_file() -> None:
    file_name = "billing-test-file.png"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await save_file(test_file, file_name)
    assert f"resources/{file_name}" in await list_files(
        FI_AWS_S3_MAIN_BUCKET, f"resources/{file_name}"
    )


async def test_search_file() -> None:
    file_name = "unittesting-test-file.csv"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await save_file(test_file, file_name)
    assert f"resources/{file_name}" in await list_files(
        FI_AWS_S3_MAIN_BUCKET, f"resources/{file_name}"
    )
    assert f"resources/{file_name}" in await search_file(file_name)


async def test_remove_file() -> None:
    file_name = "unittesting-test-file.csv"
    await remove_file(file_name)
    assert f"resources/{file_name}" not in await list_files(
        FI_AWS_S3_MAIN_BUCKET, file_name
    )
