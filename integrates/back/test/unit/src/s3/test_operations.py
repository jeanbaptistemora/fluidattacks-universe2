from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
    set_mocks_side_effects,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    UnavailabilityError,
)
import os
import pytest
from s3.operations import (
    upload_memory_file,
)
from starlette.datastructures import (
    UploadFile,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["file_name"],
    [["test-file-records.csv"]],
)
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_upload_memory_file(
    mock_get_s3_resource: AsyncMock,
    file_name: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_get_s3_resource.return_value.upload_fileobj],
        module_at_test=MODULE_AT_TEST,
        paths_list=["client.upload_fileobj"],
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await upload_memory_file(test_file, file_name)
    assert mock_get_s3_resource.return_value.upload_fileobj.call_count == 1

    with pytest.raises(ErrorUploadingFileS3):
        with open(file_location, "rb") as data:
            await upload_memory_file(data, file_name)
    assert mock_get_s3_resource.return_value.upload_fileobj.call_count == 1


@pytest.mark.parametrize(
    ["file_name"],
    [["unittesting-test-file.csv"]],
)
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_upload_memory_file_client_error(
    mock_get_s3_resource: AsyncMock,
    file_name: str,
) -> None:

    assert set_mocks_side_effects(
        mocks_args=[[file_name]],
        mocked_objects=[mock_get_s3_resource.return_value.upload_fileobj],
        module_at_test=MODULE_AT_TEST,
        paths_list=["client.upload_fileobj"],
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with pytest.raises(UnavailabilityError):
        with open(file_location, "rb") as data:
            test_file = UploadFile(data)  # type: ignore
            await upload_memory_file(test_file, file_name)
