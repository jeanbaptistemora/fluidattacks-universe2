import pytest
import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.domain.resources import validate_file_size
from app.exceptions import InvalidFileSize


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class ResourcesTests(TestCase):

    def test_validate_file_size(self):
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-vulns.yaml')
        with open(filename) as test_file:
            file_to_test = SimpleUploadedFile(test_file.name, test_file.read())
            assert validate_file_size(file_to_test, 1)
            with pytest.raises(InvalidFileSize):
                assert validate_file_size(file_to_test, 0)
