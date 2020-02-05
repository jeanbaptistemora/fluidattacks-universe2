from decimal import Decimal
from datetime import datetime

from django.test import TestCase
from pytz import timezone
from freezegun import freeze_time

from backend.domain.project import (
    get_email_recipients, validate_tags, is_alive, get_vulnerabilities,
    get_pending_closing_check, get_last_closing_vuln, get_last_closing_date,
    is_vulnerability_closed, get_max_severity, get_max_open_severity,
    get_open_vulnerability_date, get_mean_remediate, get_total_treatment,
    is_finding_in_drafts, list_drafts, list_comments, get_active_projects,
    get_alive_projects, list_findings, get_finding_project_name, get_pending_projects
)
from backend.dal.integrates_dal import DYNAMODB_RESOURCE
import backend.dal.vulnerability as vuln_dal


class ProjectTest(TestCase):

    def test_get_email_recipients(self):
        recipients = get_email_recipients('unittesting')
        assert isinstance(recipients, list)
        assert isinstance(recipients[0], str)

    def test_validate_tags(self):
        assert validate_tags(['testtag', 'this-is-ok', 'th15-4l50'])
        assert validate_tags(['this-tag-is-valid', 'but this is not']) == [
            'this-tag-is-valid']

    def test_is_alive(self):
        assert is_alive('unittesting')
        assert not is_alive('unexisting_project')

    def test_get_vulnerabilities(self):
        findings_to_get = ['463558592', '422286126']
        findings = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in findings_to_get]

        test_data = get_vulnerabilities(findings, 'openVulnerabilities')
        expected_output = 5
        assert test_data == expected_output

        test_data = get_vulnerabilities(findings, 'closedVulnerabilities')
        expected_output = 2
        assert test_data == expected_output

    def test_get_pending_closing_checks(self):
        test_data = get_pending_closing_check('unittesting')
        expected_output = 1
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
        initial_date = datetime(2019, 1, 15).date()
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

        open_vulnerability = vuln_dal.get(
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

        open_vulnerability = vuln_dal.get(
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

        open_vulnerability = vuln_dal.get(
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

    @freeze_time("2019-12-01")
    def test_get_mean_remediate(self):
        open_vuln_finding = ['463558592']
        open_finding = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in open_vuln_finding]

        test_data = get_mean_remediate(open_finding)
        expected_output = Decimal('212.0')
        assert test_data == expected_output

        closed_vuln_finding = ['457497316']
        closed_finding = [
            DYNAMODB_RESOURCE.Table('FI_findings').get_item(
                TableName='FI_findings',
                Key={'finding_id': finding_id}
            )['Item']
            for finding_id in closed_vuln_finding]

        test_data = get_mean_remediate(closed_finding)
        expected_output = 293
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
        expected_output = {'inProgress': 1, 'accepted': 4, 'undefined': 0}
        assert test_data == expected_output

    def test_is_finding_in_drafts(self):
        finding_id = '463558592'
        draft_id = '475041513'

        assert not is_finding_in_drafts(finding_id)
        assert is_finding_in_drafts(draft_id)

    def test_list_drafts(self):
        project_name = 'unittesting'
        test_data = list_drafts(project_name)
        expected_output = ['475041513', '560175507']
        assert test_data == expected_output

    def test_list_comments(self):
        project_name = 'unittesting'
        test_data = list_comments(project_name, 'admin')
        expected_output = {
            'content': 'Now we can post comments on projects',
            'parent': 0, 'created':
            '2018/12/27 16:30:28',
            'id': 1545946228675,
            'fullname': 'Miguel de Orellana',
            'email': 'unittest@fluidattacks.com', 'modified': '2018/12/27 16:30:28'
        }
        assert test_data[0] == expected_output

    def test_get_active_projects(self):
        test_data = get_active_projects()
        assert test_data is not None

    def test_get_alive_projects(self):
        test_data = get_alive_projects()
        expected_output = ['suspendedtest', 'oneshottest', 'unittesting']
        assert sorted(test_data) == sorted(expected_output)

    def test_list_findings(self):
        project_name = 'unittesting'
        test_data = list_findings(project_name)
        expected_output = [
            '422286126', '436992569', '463461507', '463558592', '457497316'
        ]
        assert expected_output == test_data

    def test_get_finding_project_name(self):
        finding_id = '475041513'
        test_data = get_finding_project_name(finding_id)
        assert test_data == 'unittesting'

    def test_pending_deletion(self):
        projects = get_pending_projects()
        projects = [project['project_name'] for project in projects]
        expected_output = ['pendingproject']
        assert expected_output == projects
