import os

import pytest
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from backend.domain import resources as resources_domain
from backend.exceptions import InvalidFileSize


class ResourcesTests(TestCase):

    def test_validate_file_size(self):
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-vulns.yaml')
        with open(filename, 'rb') as test_file:
            file_to_test = SimpleUploadedFile(test_file.name, test_file.read())
            assert resources_domain.validate_file_size(file_to_test, 1)
            with pytest.raises(InvalidFileSize):
                assert resources_domain.validate_file_size(file_to_test, 0)

    def test_has_repeated_envs(self):
        envs = [{'urlEnv': 'https://test.com/new'}]
        repeated_inputs = [
            {'urlEnv': 'https://test.com/repeated'},
            {'urlEnv': 'https://test.com/repeated'}
        ]
        repeated_envs = [{
            'urlEnv': 'https%3A%2F%2Funittesting.fluidattacks.com%2F'
        }]

        assert not resources_domain.has_repeated_envs('unittesting', envs)
        assert resources_domain.has_repeated_envs(
            'unittesting', repeated_inputs)
        assert resources_domain.has_repeated_envs('unittesting', repeated_envs)

    def test_has_repeated_repos(self):
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

        assert not resources_domain.has_repeated_repos('unittesting', repos)
        assert resources_domain.has_repeated_repos(
            'unittesting', repeated_inputs)
        assert resources_domain.has_repeated_repos(
            'unittesting', repeated_repos)
