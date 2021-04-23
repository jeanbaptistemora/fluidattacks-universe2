import os

import pytest
from starlette.datastructures import UploadFile

from custom_exceptions import InvalidFileSize
from resources import domain as resources_domain


pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_file_size():
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-vulns.yaml')
    with open(filename, 'rb') as test_file:
        file_to_test = UploadFile(test_file.name, test_file)
        assert await resources_domain.validate_file_size(file_to_test, 1)
        with pytest.raises(InvalidFileSize):
            assert await resources_domain.validate_file_size(file_to_test, 0)
