import pytest
from datetime import datetime

from django.test import TestCase

from app.domain.project import (
    get_email_recipients, validate_tags, validate_project, get_vulnerabilities,
    get_pending_closing_check, get_last_closing_vuln, get_last_closing_date)
from app.dal.integrates_dal import DYNAMODB_RESOURCE


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

    def test_get_vulnerabilities(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]

        test_data = get_vulnerabilities(findings, 'openVulnerabilities')
        expected_output = 6
        assert test_data == expected_output

        test_data = get_vulnerabilities(findings, 'closedVulnerabilities')
        expected_output = 3
        assert test_data == expected_output

    def test_get_pending_closing_checks(self):
        test_data = get_pending_closing_check('unittesting')
        expected_output = 4
        assert test_data == expected_output

    def test_get_last_closing_vuln(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]
        test_data = get_last_closing_vuln(findings)
        actual_date = datetime.now().date()
        initial_date = datetime(2019, 01, 15).date()
        expected_output = actual_date - initial_date
        assert test_data == expected_output.days
