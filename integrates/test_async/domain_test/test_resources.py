import os

import pytest
from starlette.datastructures import UploadFile

from backend.dal import project as project_dal
from backend.domain import resources as resources_domain
from backend.exceptions import InvalidFileSize

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

async def test_has_repeated_envs():
    project_name = 'unittesting'
    existing_envs = await project_dal.get_attributes(
        project_name, ['environments']
    )
    existing_envs = existing_envs.get('environments', [])
    envs = [{'urlEnv': 'https://test.com/new'}]
    repeated_inputs = [
        {'urlEnv': 'https://test.com/repeated'},
        {'urlEnv': 'https://test.com/repeated'}
    ]
    repeated_envs = [{
        'urlEnv': 'https%3A%2F%2Funittesting.fluidattacks.com%2F'
    }]

    assert not resources_domain.has_repeated_envs(
        project_name, existing_envs, envs
    )
    assert resources_domain.has_repeated_envs(
        project_name, existing_envs, repeated_inputs
    )
    assert resources_domain.has_repeated_envs(
        project_name, existing_envs, repeated_envs
    )
