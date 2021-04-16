# -*- coding: utf-8 -*-
import os
import pytest
import shutil
from collections import OrderedDict
from decimal import Decimal
from unittest.mock import patch

from freezegun import freeze_time

from back.tests.unit.utils import create_dummy_simple_session
from backend.api import get_new_context
from backend.domain import project as group_domain
from backend.scheduler import (
    calculate_vulnerabilities,
    create_data_format_chart,
    create_msj_finding_pending,
    create_register_by_week,
    create_weekly_date,
    delete_imamura_stakeholders,
    delete_obsolete_groups,
    delete_obsolete_orgs,
    extract_info_from_event_dict,
    format_vulnerabilities,
    get_accepted_vulns,
    get_by_time_range,
    get_date_last_vulns,
    get_finding_url,
    get_first_week_dates,
    get_project_indicators,
    get_status_vulns_by_time_range,
    get_unsolved_events,
    is_a_unsolved_event,
    is_not_a_fluidattacks_email,
    remove_fluid_from_recipients,
)
from data_containers.toe_lines import GitRootToeLines
from findings.dal import get_finding
from findings.domain import get_findings_by_group
from groups import domain as groups_domain
from newutils import datetime as datetime_utils
from organizations.domain import (
    get_id_by_name,
    get_pending_deletion_date_str,
    iterate_organizations,
    update_pending_deletion_date,
)
from toe.lines import domain as toe_lines_domain
from schedulers import toe_lines_etl
from users import dal as users_dal
from vulnerabilities.dal import get as get_vuln
from vulnerabilities.domain import list_vulnerabilities_async


pytestmark = [
    pytest.mark.asyncio,
]


def test_is_not_a_fluid_attacks_email():
    fluid_attacks_email = 'test@fluidattacks.com'
    not_fluid_attacks_email = 'test@test.com'
    assert is_not_a_fluidattacks_email(not_fluid_attacks_email)
    assert not is_not_a_fluidattacks_email(fluid_attacks_email)

def test_remove_fluid_from_recipients():
    emails = [
        'test@fluidattacks.com', 'test2@fluidattacks.com', 'test@test.com',
        'test2@test.com'
    ]
    test_data = remove_fluid_from_recipients(emails)
    expected_output = ['test@test.com', 'test2@test.com']
    assert test_data == expected_output

def test_is_a_unsolved_event():
    dumb_unsolved_event = {
        'id': 'testid',
        'historic_state': [{'state': 'OPEN'}, {'state': 'CREATED'}]
    }
    dumb_solved_event = {
        'id': 'testid',
        'historic_state': [
            {'state': 'OPEN'},
            {'state': 'CREATED'},
            {'state': 'CLOSED'}
        ]
    }
    assert is_a_unsolved_event(dumb_unsolved_event)
    assert not is_a_unsolved_event(dumb_solved_event)

async def test_get_unsolved_events():
    request = create_dummy_simple_session('unittest')
    project_name = 'unittesting'
    test_data = await get_unsolved_events(project_name)
    assert isinstance(test_data, list)
    assert isinstance(test_data[0], dict)
    assert [ev for ev in test_data if ev['event_id'] == '540462628']

def test_extract_info_from_event_dict():
    dumb_event_dict = {
        'id': 'testid', 'event_type': 'test', 'detail': 'detail'
    }
    test_data = extract_info_from_event_dict(dumb_event_dict)
    expected_output = {'type': 'test', 'details': 'detail'}
    assert test_data == expected_output

def test_get_finding_url():
    dumb_finding_dict = {'project_name': 'test', 'finding_id': 'test'}
    org_name = 'okada'
    group_name = 'group_test'
    test_data = get_finding_url(dumb_finding_dict, group_name, org_name)
    expected_output = (
        'https://app.fluidattacks.com/orgs/okada/groups'
        '/group_test/test/description'
    )
    assert test_data == expected_output

@freeze_time('2019-09-15')
async def test_calculate_vulnerabilities():
    context = get_new_context()
    finding_id = '436992569'
    assert await calculate_vulnerabilities(context, finding_id) == 17

async def test_get_status_vulns_by_time_range():
    released_findings = await get_findings_by_group('UNITTESTING')
    first_day = '2019-01-01 12:00:00'
    last_day = '2019-06-30 23:59:59'
    vulns = await list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in released_findings],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    test_data = get_status_vulns_by_time_range(
        vulns, first_day, last_day
    )
    expected_output = {'found': 8, 'accepted': 2, 'closed': 2}
    assert test_data == expected_output

def test_create_weekly_date():
    first_date = '2019-09-19 13:23:32'
    test_data = create_weekly_date(first_date)
    expected_output = 'Sep 16 - 22, 2019'
    assert test_data == expected_output

async def test_get_accepted_vulns():
    released_findings = await get_findings_by_group('UNITTESTING')
    last_day = '2019-06-30 23:59:59'
    vulns = await list_vulnerabilities_async(
        [str(finding['finding_id']) for finding in released_findings],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    test_data = sum([get_accepted_vulns(vuln, last_day) for vuln in vulns])
    expected_output = 2
    assert test_data == expected_output

async def test_get_by_time_range():
    last_day = '2020-09-09 23:59:59'
    vuln = await get_vuln('80d6a69f-a376-46be-98cd-2fdedcffdcc0')
    test_data = get_by_time_range(
        vuln[0], last_day
    )
    expected_output = 1
    assert test_data == expected_output

async def test_create_register_by_week():
    context = get_new_context()
    project_name = 'unittesting'
    test_data = await create_register_by_week(context, project_name)
    assert isinstance(test_data, list)
    for item in test_data:
        assert isinstance(item, list)
        assert isinstance(item[0], dict)
        assert item[0] is not None

def test_create_data_format_chart():
    registers = OrderedDict(
        [('Sep 24 - 30, 2018',
            {'found': 2, 'accepted': 0, 'closed': 0, 'assumed_closed': 0,
            'opened': 2})]
    )
    test_data = create_data_format_chart(registers)
    expected_output = [
        [{'y': 2, 'x': 'Sep 24 - 30, 2018'}],
        [{'y': 0, 'x': 'Sep 24 - 30, 2018'}],
        [{'y': 0, 'x': 'Sep 24 - 30, 2018'}],
        [{'y': 0, 'x': 'Sep 24 - 30, 2018'}],
        [{'y': 2, 'x': 'Sep 24 - 30, 2018'}],
    ]
    assert test_data == expected_output

async def test_get_first_week_dates():
    vulns = await list_vulnerabilities_async(
        ['422286126'],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    test_data = get_first_week_dates(vulns)
    expected_output = ('2019-12-30 00:00:00', '2020-01-05 23:59:59')
    assert test_data == expected_output

async def test_get_date_last_vulns():
    vulns = await list_vulnerabilities_async(
        ['422286126'],
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True
    )
    test_data = get_date_last_vulns(vulns)
    expected_output = '2020-09-07 16:01:26'
    assert test_data == expected_output

async def test_format_vulnerabilities():
    act_finding = await get_finding('422286126')
    positive_delta = 1
    neutral_delta = 0
    negative_delta = -1

    test_data = format_vulnerabilities(positive_delta, act_finding)
    expected_output = 'F060. Insecure exceptions (+1)'
    assert test_data == expected_output

    test_data = format_vulnerabilities(neutral_delta, act_finding)
    expected_output = ''
    assert test_data == expected_output

    test_data = format_vulnerabilities(negative_delta, act_finding)
    expected_output = 'F060. Insecure exceptions (-1)'
    assert test_data == expected_output

async def test_create_msj_finding_pending():
    context = get_new_context()
    not_new_treatment_finding = await get_finding('422286126')
    new_treatment_finding = await get_finding('436992569')

    test_data = await create_msj_finding_pending(context, not_new_treatment_finding)
    expected_output = ''
    assert test_data == expected_output

    test_data = await create_msj_finding_pending(context, new_treatment_finding)
    expected_output = u'F038. Fuga de información de negocio'
    assert expected_output in test_data

async def test_get_project_indicators():
    group_name = 'unittesting'
    findings = await get_findings_by_group(group_name)
    vulns = await list_vulnerabilities_async(
        [finding['finding_id'] for finding in findings]
    )
    test_data = await get_project_indicators(group_name)
    over_time = [element[-12:] for element in test_data['remediated_over_time']]
    found = over_time[0][-1]['y']
    closed = over_time[1][-1]['y']
    accepted = over_time[2][-1]['y']

    assert isinstance(test_data, dict)
    assert len(test_data) == 17
    assert test_data['max_open_severity'] == Decimal(6.3).quantize(Decimal('0.1'))
    assert found == len(
        [vuln for vuln in vulns if vuln['historic_state'][-1].get('state') != 'DELETED']
    )
    assert accepted == len(
        [vuln for vuln in vulns
         if vuln.get('historic_treatment', [{}])[-1].get(
             'treatment'
         ) in {'ACCEPTED', 'ACCEPTED_UNDEFINED'}
         and vuln['historic_state'][-1].get('state') == 'open']
    )
    assert closed == len(
        [vuln for vuln in vulns if vuln['historic_state'][-1].get('state') == 'closed']
    )

@pytest.mark.changes_db
@freeze_time("2019-12-01")
async def test_delete_obsolete_orgs():
    org_id = 'ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448'
    org_name = 'kiba'
    org_ids = []
    async for organization_id, _ in iterate_organizations():
        org_ids.append(organization_id)
    assert org_id in org_ids
    assert len(org_ids) == 9

    now_str = datetime_utils.get_as_str(
         datetime_utils.get_now()
    )
    await update_pending_deletion_date(
        org_id,
        org_name,
        now_str
    )
    await delete_obsolete_orgs()
    new_org_ids = []
    async for organization_id, _ in iterate_organizations():
        new_org_ids.append(organization_id)
    assert org_id not in new_org_ids
    assert len(new_org_ids) == 8

    org_id = 'ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de'
    org_pending_deletion_date = await get_pending_deletion_date_str(org_id)
    assert org_pending_deletion_date == '2020-01-29 19:00:00'


@pytest.mark.changes_db
@freeze_time("2021-01-01")
async def test_delete_imamura_stakeholders():
    org_name = 'imamura'
    org_id = await get_id_by_name(org_name)
    loaders = get_new_context()
    org_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await org_stakeholders_loader.load(org_id)
    org_stakeholders_emails = [
        stakeholder['email']
        for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == [
        'deleteimamura@fluidattacks.com',
        'nodeleteimamura@fluidattacks.com',
    ]
    delete_stakeholder = await users_dal.get(
        'deleteimamura@fluidattacks.com'
    )
    delete_stakeholder_exists = bool(delete_stakeholder)
    assert delete_stakeholder_exists
    nodelete_stakeholder = await users_dal.get(
        'nodeleteimamura@fluidattacks.com'
    )
    nodelete_stakeholder_exists = bool(nodelete_stakeholder)
    assert nodelete_stakeholder_exists

    await delete_imamura_stakeholders()

    loaders = get_new_context()
    org_stakeholders_loader = loaders.organization_stakeholders
    org_stakeholders = await org_stakeholders_loader.load(org_id)
    org_stakeholders_emails = [
        stakeholder['email']
        for stakeholder in org_stakeholders
    ]
    assert org_stakeholders_emails == ['nodeleteimamura@fluidattacks.com']
    delete_stakeholder = await users_dal.get(
        'deleteimamura@fluidattacks.com'
    )
    delete_stakeholder_exists = bool(delete_stakeholder)
    assert not delete_stakeholder_exists
    nodelete_stakeholder = await users_dal.get(
        'nodeleteimamura@fluidattacks.com'
    )
    nodelete_stakeholder_exists = bool(nodelete_stakeholder)
    assert nodelete_stakeholder_exists


@pytest.mark.changes_db
async def test_delete_obsolete_groups():
    group_attributes = {
        'project_name',
        'project_status',
        'pending_deletion_date'
    }
    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 13
    expected_groups = [
        {
            'project_status': 'SUSPENDED',
            'project_name': 'setpendingdeletion',
        },
        {
            'project_name': 'deletegroup',
            'project_status': 'ACTIVE',
            'pending_deletion_date': '2020-12-22 14:36:29'
        },
    ]
    for expected_group in expected_groups:
        assert expected_group in alive_groups

    await delete_obsolete_groups()

    alive_groups = await groups_domain.get_alive_groups(group_attributes)
    assert len(alive_groups) == 12
    groups = await group_domain.get_all(group_attributes)
    setpendingdeletion = [
        group
        for group in groups
        if group['project_name'] == 'setpendingdeletion'
    ][0]
    assert setpendingdeletion['project_status'] == 'SUSPENDED'
    assert 'pending_deletion_date' in setpendingdeletion
    deletegroup = [
        group
        for group in groups
        if group['project_name'] == 'deletegroup'
    ][0]
    assert deletegroup['project_status'] == 'DELETED'


@pytest.mark.changes_db
async def test_toe_lines_etl():
    def clone_services_repository_mock(path):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'mock/test_lines.csv')
        os.makedirs(f'{path}/groups/unittesting/toe')
        shutil.copy2(filename, f'{path}/groups/unittesting/toe/lines.csv')

    group_name = 'unittesting'
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert group_toe_lines == (
        GitRootToeLines(
            comments='comment test',
            filename='product/test/test#.config',
            group_name='unittesting',
            loc=8,
            modified_commit='983466z',
            modified_date='2019-08-01T00:00:00-05:00',
            root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
            tested_date='2021-02-28T00:00:00-05:00',
            tested_lines=4
        ),
        GitRootToeLines(
            comments='comment test',
            filename='integrates_1/test2/test.sh',
            group_name='unittesting',
            loc=120,
            modified_commit='273412t',
            modified_date='2020-11-19T00:00:00-05:00',
            root_id='765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            tested_date='2021-01-20T00:00:00-05:00',
            tested_lines=172
        )
    )

    with patch(
        'newutils.git.clone_services_repository',
        wraps=clone_services_repository_mock
    ):
        await toe_lines_etl.main()

    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert group_toe_lines == (
        GitRootToeLines(
            comments='comment test 2',
            filename='product/test/test#.config',
            group_name='unittesting',
            loc=8,
            modified_commit='983466z',
            modified_date='2019-08-01T00:00:00-05:00',
            root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
            tested_date='2021-02-28T00:00:00-05:00',
            tested_lines=4
        ),
        GitRootToeLines(
            comments='comment test',
            filename='integrates_1/test3/test.sh',
            group_name='unittesting',
            loc=12,
            modified_commit='742412r',
            modified_date='2020-11-19T00:00:00-05:00',
            root_id='765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            tested_date='2021-01-22T00:00:00-05:00',
            tested_lines=88
        )
    )
