import os

import pytest
from django.test import TestCase
from starlette.datastructures import UploadFile

from backend.dal import project as project_dal
from backend.domain import resources as resources_domain
from backend.exceptions import InvalidFileSize

pytestmark = [
    pytest.mark.asyncio,
]


class ResourcesTests(TestCase):

    async def test_validate_file_size(self):
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-vulns.yaml')
        with open(filename, 'rb') as test_file:
            file_to_test = UploadFile(test_file.name, test_file)
            assert await resources_domain.validate_file_size(file_to_test, 1)
            with pytest.raises(InvalidFileSize):
                assert await resources_domain.validate_file_size(file_to_test, 0)

    async def test_has_repeated_envs(self):
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

    async def test_has_repeated_repos(self):
        project_name = 'unittesting'
        existing_repos = await project_dal.get_attributes(
            project_name, ['repositories']
        )
        existing_repos = existing_repos.get('repositories', [])
        repos = [
            {
                'urlRepo': 'https://gitlab.com/test/new.git',
                'branch': 'master',
                'protocol': 'HTTPS'
            }
        ]
        repeated_inputs = [
            {
                'urlRepo': 'https://gitlab.com/test/repeated.git',
                'branch': 'master',
                'protocol': 'HTTPS'
            },
            {
                'urlRepo': 'https://gitlab.com/test/repeated.git',
                'branch': 'master',
                'protocol': 'HTTPS'
            }
        ]
        repeated_repos = [
            {
                'urlRepo': 'https%3A%2F%2Fgitlab.com%2Ffluidsignal%2Funittest',
                'branch': 'master',
                'protocol': 'HTTPS'
            }
        ]

        assert not resources_domain.has_repeated_repos(
            project_name, existing_repos, repos
        )
        assert resources_domain.has_repeated_repos(
            project_name, existing_repos, repeated_inputs
        )
        assert resources_domain.has_repeated_repos(
            project_name, existing_repos, repeated_repos
        )
