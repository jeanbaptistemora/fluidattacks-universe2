import time
from decimal import Decimal
from datetime import datetime

from django.test import TestCase
from pytz import timezone
from freezegun import freeze_time
import pytest

from backend.dal.helpers import dynamodb
from backend.domain.project import (
    add_comment,
    get_email_recipients, validate_tags, is_alive, get_vulnerabilities,
    get_pending_closing_check, get_last_closing_vuln, get_last_closing_date,
    is_vulnerability_closed, get_max_open_severity,
    get_open_vulnerability_date, get_mean_remediate, get_total_treatment,
    list_drafts, list_comments, get_active_projects,
    get_alive_projects, list_findings, get_finding_project_name, get_pending_to_delete,
    get_mean_remediate_severity, remove_access, validate_project_services_config
)
from backend.exceptions import (
    InvalidProjectServicesConfig, RepeatedValues
)
import backend.dal.vulnerability as vuln_dal

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore


class ProjectTest(TestCase):

    def test_get_email_recipients(self):
        recipients = get_email_recipients('unittesting')
        assert isinstance(recipients, list)
        assert isinstance(recipients[0], str)

    def test_validate_project_services_config(self):
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(True, False, True)
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(False, False, True)
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(False, True, False)

    def test_remove_access(self):
        assert remove_access('unittest', 'unittesting')
        assert not remove_access('', '')

    def test_validate_tags(self):
        assert validate_tags(
            'unittesting', ['testtag', 'this-is-ok', 'th15-4l50'])
        assert validate_tags(
            'unittesting', ['this-tag-is-valid', 'but this is not']) == [
            'this-tag-is-valid']
        with pytest.raises(RepeatedValues):
            assert validate_tags(
                'unittesting', ['same-name', 'same-name', 'another-one'])
        with pytest.raises(RepeatedValues):
            assert validate_tags('unittesting', ['test-projects'])

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
        expected_output = 2
        assert test_data == expected_output

    @pytest.mark.skip(
        reason="https://gitlab.com/fluidattacks/integrates/issues/1761")
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
        expected_output = \
            {'inProgress': 1, 'accepted': 4, 'acceptedUndefined': 0, 'undefined': 0}
        assert test_data == expected_output


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
            'parent': 0,
            'created': '2018/12/27 16:30:28',
            'id': 1545946228675,
            'fullname': 'Hacker at Fluid Attacks',
            'email': 'unittest@fluidattacks.com',
            'modified': '2018/12/27 16:30:28',
        }
        assert test_data[0] == expected_output

    def test_add_comment(self):
        project_name = 'unittesting'
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'user_id': comment_id,
            'content': 'Test comment',
            'created': current_time,
            'fullname': 'unittesting',
            'modified': current_time,
            'parent': '0'
        }
        assert add_comment(project_name, 'unittest@fluidattacks.com', comment_data)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data['created'] = current_time
        comment_data['modified'] = current_time
        comment_data['parent'] = str(comment_id)
        assert add_comment(project_name, 'unittest@fluidattacks.com', comment_data)

    def test_get_active_projects(self):
        test_data = get_active_projects()
        assert test_data is not None

    def test_get_alive_projects(self):
        test_data = get_alive_projects()
        expected_output = ['suspendedtest', 'oneshottest', 'unittesting', 'continuoustesting']
        assert sorted(test_data) == sorted(expected_output)

    def test_list_findings(self):
        project_name = 'unittesting'
        test_data = list_findings(project_name)
        expected_output = [
            '988493279', '422286126', '436992569', '463461507', '463558592', '457497316'
        ]
        assert expected_output == test_data

    def test_get_finding_project_name(self):
        finding_id = '475041513'
        test_data = get_finding_project_name(finding_id)
        assert test_data == 'unittesting'

    def test_get_pending_to_delete(self):
        projects = get_pending_to_delete()
        projects = [project['project_name'] for project in projects]
        expected_output = ['pendingproject']
        assert expected_output == projects

    @pytest.mark.skip(
        reason="https://gitlab.com/fluidattacks/integrates/issues/1761")
    @freeze_time("2020-04-12")
    def test_get_mean_remediate_severity(self):
        project_name = 'unittesting'
        min_severity = 0.1
        max_severity = 3.9
        mean_remediate_low_severity = get_mean_remediate_severity(
            project_name, min_severity, max_severity)
        expected_output = (219, 232)
        assert mean_remediate_low_severity in expected_output
        min_severity = 4
        max_severity = 6.9
        mean_remediate_medium_severity = get_mean_remediate_severity(
            project_name, min_severity, max_severity)
        expected_output = 287
        assert mean_remediate_medium_severity == expected_output
