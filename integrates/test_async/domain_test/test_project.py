import time
from decimal import Decimal
from datetime import datetime

from aioextensions import (
    collect,
)
from django.test import TestCase
from pytz import timezone
from freezegun import freeze_time
import pytest

from backend.dal.helpers import dynamodb
from backend.domain.project import (
    add_comment,
    edit, validate_tags, is_alive,
    get_pending_closing_check, get_last_closing_vuln_info, get_last_closing_date,
    is_vulnerability_closed, get_max_open_severity,
    get_open_vulnerability_date, get_mean_remediate, get_total_treatment,
    get_users, get_description, get_pending_verification_findings,
    list_drafts, list_comments, get_active_projects, get_managers, list_events,
    get_alive_projects, list_findings, get_pending_to_delete,
    get_mean_remediate_severity, remove_access, validate_project_services_config,
    create_project, total_vulnerabilities,
    get_open_vulnerabilities, get_closed_vulnerabilities, get_open_finding,
    remove_project, get_closers
)
from backend.exceptions import (
    InvalidProjectServicesConfig, RepeatedValues
)
from backend.dal import (
    finding as finding_dal,
    project as project_dal,
    vulnerability as vuln_dal,
    available_name as available_name_dal
)

from backend_new import settings

pytestmark = [
    pytest.mark.asyncio,
]


class ProjectTest(TestCase):

    def test_validate_project_services_config(self):
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(True, True, False, False)
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(True, False, True, True)
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(True, True, True, False)
        with pytest.raises(InvalidProjectServicesConfig):
            validate_project_services_config(False, False, True, True)

    @pytest.mark.changes_db
    async def test_remove_access(self):
        assert await remove_access('unittest', 'unittesting')
        assert not await remove_access('', '')

    async def test_validate_tags(self):
        assert await validate_tags(
            'unittesting', ['testtag', 'this-is-ok', 'th15-4l50'])
        assert await validate_tags(
            'unittesting', ['this-tag-is-valid', 'but this is not']) == [
            'this-tag-is-valid']
        with pytest.raises(RepeatedValues):
            assert await validate_tags(
                'unittesting', ['same-name', 'same-name', 'another-one'])
        with pytest.raises(RepeatedValues):
            assert await validate_tags('unittesting', ['test-projects'])

    async def test_is_alive(self):
        assert await is_alive('unittesting')
        assert not await is_alive('unexisting_project')

    async def test_get_pending_closing_checks(self):
        test_data = await get_pending_closing_check('unittesting')
        expected_output = 2
        assert test_data == expected_output

    async def test_get_last_closing_vuln(self):
        findings_to_get = ['463558592', '422286126']
        findings = await collect(
            finding_dal.get_finding(finding_id)
            for finding_id in findings_to_get
        )
        test_data = await get_last_closing_vuln_info(findings)
        tzn = timezone(settings.TIME_ZONE)
        actual_date = datetime.now(tz=tzn).date()
        initial_date = datetime(2019, 1, 15).date()
        assert test_data[0] == (actual_date - initial_date).days
        assert test_data[1]['UUID'] == '6f023c26-5b10-4ded-aa27-bb563c2206ab'
        assert test_data[1]['finding_id'] == "463558592"

    async def test_get_last_closing_date(self):
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

        open_vulnerability = await vuln_dal.get(
            '80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )

        test_data = get_last_closing_date(closed_vulnerability)
        closing_date = datetime(2019, 1, 8).date()
        assert test_data == closing_date

        test_data = get_last_closing_date(open_vulnerability[0])
        assert test_data is None

    async def test_is_vulnerability_closed(self):
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

        open_vulnerability = await vuln_dal.get(
            '80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )

        assert is_vulnerability_closed(closed_vulnerability)
        assert not is_vulnerability_closed(open_vulnerability[0])

    async def test_get_max_open_severity(self):
        findings_to_get = ['463558592', '422286126']
        findings = await collect(
            finding_dal.get_finding(finding_id)
            for finding_id in findings_to_get
        )
        test_data = await get_max_open_severity(findings)
        assert test_data[0] == Decimal(4.3).quantize(Decimal('0.1'))
        assert test_data[1]['finding_id'] == "463558592"

    async def test_get_open_vulnerabilities(self):
        project_name = 'unittesting'
        expected_output = 32
        assert await get_open_vulnerabilities(project_name) == expected_output

    async def test_get_closed_vulnerabilities(self):
        project_name = 'unittesting'
        expected_output = 8
        assert await get_closed_vulnerabilities(project_name) == expected_output

    async def test_get_open_finding(self):
        project_name = 'unittesting'
        expected_output = 5
        assert await get_open_finding(project_name) == expected_output

    async def test_get_open_vulnerability_date(self):
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

        open_vulnerability = await vuln_dal.get(
            '80d6a69f-a376-46be-98cd-2fdedcffdcc0'
        )

        test_data = get_open_vulnerability_date(open_vulnerability[0])
        expected_output = datetime(2018, 9, 28).date()
        assert test_data == expected_output

        test_data = get_open_vulnerability_date(closed_vulnerability)
        assert test_data is None

    @freeze_time("2019-12-01")
    async def test_get_mean_remediate(self):
        open_vuln_finding = '463558592'
        open_finding = await finding_dal.get_finding(open_vuln_finding)

        test_data = await get_mean_remediate([open_finding])
        expected_output = Decimal('212.0')
        assert test_data == expected_output

        closed_vuln_finding = '457497316'
        closed_finding = await finding_dal.get_finding(closed_vuln_finding)

        test_data = await get_mean_remediate([closed_finding])
        expected_output = 293
        assert test_data == expected_output

    async def test_get_total_treatment(self):
        findings_to_get = ['463558592', '422286126']
        findings = await collect(
            finding_dal.get_finding(finding_id)
            for finding_id in findings_to_get
        )
        test_data = await get_total_treatment(findings)
        expected_output = \
            {'inProgress': 2, 'accepted': 4, 'acceptedUndefined': 0, 'undefined': 0}
        assert test_data == expected_output

    async def test_list_drafts(self):
        project_name = 'unittesting'
        test_data = await list_drafts([project_name])
        expected_output = ['560175507']
        assert expected_output == test_data[0]

    async def test_list_comments(self):
        project_name = 'unittesting'
        test_data = await list_comments(project_name, 'admin')
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

    @pytest.mark.changes_db
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

    async def test_get_active_projects(self):
        test_data = await get_active_projects()
        assert test_data is not None

    async def test_get_alive_projects(self):
        test_data = await get_alive_projects()
        expected_output = ['suspendedtest', 'oneshottest', 'unittesting', 'continuoustesting']
        assert sorted(test_data) == sorted(expected_output)

    async def test_list_findings(self):
        project_name = 'unittesting'
        test_data = await list_findings([project_name])
        expected_output = [
            '988493279', '422286126', '436992569', '463461507', '463558592', '457497316'
        ]
        assert expected_output == test_data[0]

    async def test_list_drafts_deleted(self):
        projects_name = ['continuoustesting']
        test_data = await list_drafts(projects_name)
        expected_output = ['818828206', '836530833', '475041524']
        assert sorted(expected_output) == sorted(test_data[0])
        test_data = await list_drafts(projects_name, should_list_deleted=True)
        expected_output = ['818828206', '836530833', '475041524', '991607942']
        assert sorted(expected_output) == sorted(test_data[0])

    async def test_list_events(self):
        project_name = 'unittesting'
        expected_output = ['540462628', '538745942', '463578352', '484763304', '418900971']
        assert expected_output == await list_events(project_name)

    async def test_get_managers(self):
        project_name = 'unittesting'
        expected_output = [
            'integratesuser@gmail.com', 'continuoushacking@gmail.com', 'continuoushack2@gmail.com'
        ]
        assert expected_output == await get_managers(project_name)

    async def test_get_description(self):
        project_name = 'unittesting'
        expected_output = 'Integrates unit test project'
        assert expected_output == await get_description(project_name)

    async def test_get_users(self):
        project_name = 'unittesting'
        expected_output = [
            'integratescloser@fluidattacks.com',
            'integratesmanager@gmail.com',
            'unittest@fluidattacks.com',
            'unittest2@fluidattacks.com',
            'integratesexecutive@gmail.com',
            'integratescustomer@gmail.com',
            'integratesuser@gmail.com',
            'integratesanalyst@fluidattacks.com',
            'continuoushacking@gmail.com',
            'continuoushack2@gmail.com'
        ]
        assert expected_output == await get_users(project_name)

    async def test_get_pending_to_delete(self):
        projects = await get_pending_to_delete()
        projects = [project['project_name'] for project in projects]
        expected_output = ['pendingproject']
        assert expected_output == projects

    async def test_get_closers(self):
        await get_closers('oneshottest') == 'integratesanalyst@fluidattacks.com'

    @freeze_time("2020-04-12")
    async def test_get_mean_remediate_severity(self):
        project_name = 'unittesting'
        min_severity = 0.1
        max_severity = 3.9
        mean_remediate_low_severity = await get_mean_remediate_severity(
            project_name, min_severity, max_severity)
        expected_output = (212, 232)
        assert mean_remediate_low_severity in expected_output
        min_severity = 4
        max_severity = 6.9
        mean_remediate_medium_severity = await get_mean_remediate_severity(
            project_name, min_severity, max_severity)
        expected_output = 287
        assert mean_remediate_medium_severity == expected_output

    @pytest.mark.changes_db
    async def test_create_project_not_user_admin(self):
        await available_name_dal.create('NEWAVAILABLENAME', 'group')
        user_email = 'integratesuser@gmail.com'
        user_role = 'customeradmin'
        test_data = await create_project(
            user_email=user_email,
            user_role=user_role,
            project_name='NEWAVAILABLENAME',
            organization='okada',
            description='This is a new project',
            has_drills=True,
            has_forces=True,
            subscription='continuous'
        )
        expected_output = True
        assert test_data == expected_output

    @pytest.mark.changes_db
    async def test_remove_group(self):
        group_name = 'pendingproject'
        assert len(await project_dal.get_comments(group_name)) >= 1
        test_data = await remove_project(group_name)
        assert all(test_data)
        assert len(await project_dal.get_comments(group_name)) == 0

@pytest.mark.changes_db
@pytest.mark.parametrize(
    ['group_name', 'subscription', 'has_drills', 'has_forces', 'has_integrates', 'expected'],
    [
        ['unittesting', 'continuous', True, True, True, True],
        ['oneshottest', 'oneshot', False, False, True, True],
        ['not-exists', 'continuous', True, True, True, False],
        ['not-exists', 'continuous', False, False, False, False],
    ]
)
async def test_edit(
    group_name: str,
    subscription: str,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    expected: bool,
):
    assert expected == await edit(
        comments='',
        group_name=group_name,
        subscription=subscription,
        has_drills=has_drills,
        has_forces=has_forces,
        has_integrates=has_integrates,
        reason='',
        requester_email='test@test.test'
    )

async def test_get_pending_verification_findings():
    project_name = 'unittesting'
    findings = await get_pending_verification_findings(project_name)
    assert len(findings) >= 1
    assert 'finding' in findings[0]
    assert 'finding_id' in findings[0]
    assert 'project_name' in findings[0]
