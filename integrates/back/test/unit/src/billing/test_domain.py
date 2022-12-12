from billing.domain import (
    remove_file,
    save_file,
    search_file,
)
from mypy_boto3_s3 import (
    S3Client,
)
import os
import pytest
from s3.operations import (
    list_files,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)
from unittest.mock import (
    AsyncMock,
)

pytestmark = [
    pytest.mark.asyncio,
]


@mock.patch(
    "s3.operations.get_s3_resource",
    new_callable=AsyncMock,
)
async def test_save_file(
    mock_s3_client: AsyncMock, s3_client: S3Client
) -> None:
    def mock_upload_fileobj(*args: Any) -> Any:
        return s3_client.upload_fileobj(*args)

    def mock_list_objects_v2(**kwargs: Any) -> Any:
        return s3_client.list_objects_v2(**kwargs)

    file_name = "billing-test-file.png"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        mock_s3_client.return_value.upload_fileobj.side_effect = (
            mock_upload_fileobj
        )
        await save_file(test_file, file_name)
    mock_s3_client.return_value.list_objects_v2.side_effect = (
        mock_list_objects_v2
    )
    assert f"resources/{file_name}" in await list_files(
        f"resources/{file_name}"
    )
    assert mock_s3_client.call_count == 2


@mock.patch(
    "s3.operations.get_s3_resource",
    new_callable=AsyncMock,
)
async def test_search_file(
    mock_s3_client: AsyncMock, s3_client: S3Client
) -> None:
    def mock_upload_fileobj(*args: Any) -> Any:
        return s3_client.upload_fileobj(*args)

    def mock_list_objects_v2(**kwargs: Any) -> Any:
        return s3_client.list_objects_v2(**kwargs)

    file_name = "unittesting-test-file.csv"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        mock_s3_client.return_value.upload_fileobj.side_effect = (
            mock_upload_fileobj
        )
        await save_file(test_file, file_name)
    mock_s3_client.return_value.list_objects_v2.side_effect = (
        mock_list_objects_v2
    )
    assert f"resources/{file_name}" in await search_file(file_name)
    assert mock_s3_client.call_count == 2


@mock.patch(
    "s3.operations.get_s3_resource",
    new_callable=AsyncMock,
)
async def test_remove_file(
    mock_s3_client: AsyncMock, s3_client: S3Client
) -> None:
    def mock_delete_object(**kwargs: Any) -> Any:
        return s3_client.delete_object(**kwargs)

    def mock_list_objects_v2(**kwargs: Any) -> Any:
        return s3_client.list_objects_v2(**kwargs)

    file_name = "unittesting-test-file.csv"
    mock_s3_client.return_value.delete_object.side_effect = mock_delete_object
    await remove_file(file_name)
    mock_s3_client.return_value.list_objects_v2.side_effect = (
        mock_list_objects_v2
    )
    assert f"resources/{file_name}" not in await list_files(file_name)
