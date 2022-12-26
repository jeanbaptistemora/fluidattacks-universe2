# pylint: disable=import-error
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from billing.domain import (
    remove_file,
    save_file,
    search_file,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(get_mocked_path("s3_ops.upload_memory_file"), new_callable=AsyncMock)
async def test_save_file(
    mock_s3_ops_upload_memory_file: AsyncMock, file_name: str
) -> None:
    mock_s3_ops_upload_memory_file.return_value = get_mock_response(
        get_mocked_path("s3_ops.upload_memory_file"),
        json.dumps([file_name]),
    )
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await save_file(test_file, file_name)
    assert mock_s3_ops_upload_memory_file.called is True


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(get_mocked_path("s3_ops.list_files"), new_callable=AsyncMock)
async def test_search_file(
    mock_s3_ops_list_files: AsyncMock, file_name: str
) -> None:
    mock_s3_ops_list_files.return_value = get_mock_response(
        get_mocked_path("s3_ops.list_files"),
        json.dumps([file_name]),
    )
    assert file_name in await search_file(file_name)
    assert mock_s3_ops_list_files.called is True


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(get_mocked_path("s3_ops.remove_file"), new_callable=AsyncMock)
async def test_remove_file(
    mock_s3_ops_remove_file: AsyncMock, file_name: str
) -> None:
    mock_s3_ops_remove_file.return_value = get_mock_response(
        get_mocked_path("s3_ops.remove_file"),
        json.dumps([file_name]),
    )
    await remove_file(file_name)
    assert mock_s3_ops_remove_file.called is True
