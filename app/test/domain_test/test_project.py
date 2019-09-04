from decimal import Decimal
import pytest
from pytz import timezone
from datetime import datetime

from django.test import TestCase

from app.domain.project import (
    get_email_recipients, validate_tags, validate_project, get_vulnerabilities,
    get_pending_closing_check, get_last_closing_vuln, get_last_closing_date,
    is_vulnerability_closed, get_max_severity, get_max_open_severity,
    get_open_vulnerability_date, get_mean_remediate, get_total_treatment)
from app.dal.integrates_dal import DYNAMODB_RESOURCE, get_vulnerability_dynamo


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
        expected_output = 2
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

    def test_get_last_closing_date(self):
        closed_vulnerability = {
            'specific': 'phone',
            'finding_id': '422286126',
            'UUID': '80d6a69f-a376-46be-98cd-2fdedcffdcc0',
            'treatment_manager': 'manager@test.com',
            'historic_state': [
                {'date': '2018-09-28 10:32:58', 'state': 'open'},
                {'date': '2019-01-08 16:01:26', 'state': 'closed'}],
            'treatment_justification': 'Test 123',
            'vuln_type': 'inputs',
            'treatment': 'IN PROGRESS',
            'where': 'https://example.com',
            'analyst': 'testanalyst@test.com'
        }

        open_vulnerability = get_vulnerability_dynamo(
            finding_id='422286126',
            vuln_type='inputs',
            where='https://example.com',
            uuid='80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )[0]

        test_data = get_last_closing_date(closed_vulnerability)
        closing_date = datetime(2019, 1, 8).date()
        assert test_data == closing_date

        test_data = get_last_closing_date(open_vulnerability)
        assert test_data is None

    def test_is_vulnerability_closed(self):
        closed_vulnerability = {
            'specific': 'phone',
            'finding_id': '422286126',
            'UUID': '80d6a69f-a376-46be-98cd-2fdedcffdcc0',
            'treatment_manager': 'manager@test.com',
            'historic_state': [
                {'date': '2018-09-28 10:32:58', 'state': 'open'},
                {'date': '2019-01-08 16:01:26', 'state': 'closed'}],
            'treatment_justification': 'Test 123',
            'vuln_type': 'inputs',
            'treatment': 'IN PROGRESS',
            'where': 'https://example.com',
            'analyst': 'testanalyst@test.com'
        }

        open_vulnerability = get_vulnerability_dynamo(
            finding_id='422286126',
            vuln_type='inputs',
            where='https://example.com',
            uuid='80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )[0]

        assert is_vulnerability_closed(closed_vulnerability)
        assert not is_vulnerability_closed(open_vulnerability)

    def test_get_max_severity(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]
        test_data = get_max_severity(findings)
        expected_output = Decimal(4.3).quantize(Decimal('0.1'))
        assert test_data == expected_output

    def test_get_max_open_severity(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]
        test_data = get_max_open_severity(findings)
        expected_output = Decimal(4.3).quantize(Decimal('0.1'))
        assert test_data == expected_output

    def test_get_open_vulnerability_date(self):
        closed_vulnerability = {
            'specific': 'phone',
            'finding_id': '422286126',
            'UUID': '80d6a69f-a376-46be-98cd-2fdedcffdcc0',
            'treatment_manager': 'manager@test.test',
            'historic_state': [
                {'date': '2019-01-08 16:01:26', 'state': 'closed'}
            ],
            'treatment_justification': 'Test 123',
            'vuln_type': 'inputs',
            'treatment': 'IN PROGRESS',
            'where': 'https://example.com',
            'analyst': 'testanalyst@test.com'
        }

        open_vulnerability = get_vulnerability_dynamo(
            finding_id='422286126',
            vuln_type='inputs',
            where='https://example.com',
            uuid='80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )[0]

        test_data = get_open_vulnerability_date(open_vulnerability)
        expected_output = datetime(2018, 9, 28).date()
        assert test_data == expected_output

        test_data = get_open_vulnerability_date(closed_vulnerability)
        assert test_data is None

    def test_get_mean_remediate(self):
        open_vuln_finding = ['463558592']
        open_finding = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in open_vuln_finding]
    
        test_data = get_mean_remediate(open_finding)
        current_day = datetime.now(tz=timezone('America/Bogota')).date()
        expected_output = int((current_day - datetime(2019, 3, 22).date()).days)
        assert test_data == expected_output
        
        closed_vuln_finding = ['457497316']
        closed_finding = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in closed_vuln_finding]

        test_data = get_mean_remediate(closed_finding)
        expected_output = 280
        assert test_data == expected_output

    def test_get_total_treatment(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]
        test_data = get_total_treatment(findings)
        expected_output = {'inProgress': 1, 'accepted': 5, 'undefined': 0}
        assert test_data == expected_output
