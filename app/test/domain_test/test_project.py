import pytest

from app.domain.project import (get_email_recipients, validate_tags,
    validate_project, get_vulnerabilities)

from django.test import TestCase


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class ProjectTest(TestCase):

    def test_get_email_recipients(self):
        recipients = get_email_recipients('unittesting')
        expected_recipients = ['dvasquez@fluidattacks.com']
        assert recipients == expected_recipients

    def test_validate_tags(self):
        assert validate_tags(['testtag', 'this-is-ok', 'th15-4l50'])
        assert validate_tags(['this-tag-is-valid', 'but this is not']) == [
            'this-tag-is-valid']

    def test_validate_project(self):
        assert validate_project('unittesting')
        assert not validate_project('unexisting_project')
