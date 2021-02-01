# -*- coding: utf-8 -*-
import pytest
from collections import OrderedDict
from decimal import Decimal

from freezegun import freeze_time
from jose import jwt

from backend.dal.finding import get_finding
from backend.dal.vulnerability import get as get_vuln
from backend.domain.organization import (
    get_pending_deletion_date_str,
    iterate_organizations,
    update_pending_deletion_date,
)
from backend.domain.finding import get_findings_by_group
from backend.domain.vulnerability import list_vulnerabilities_async
from backend.scheduler import (
    is_not_a_fluidattacks_email, remove_fluid_from_recipients,
    is_a_unsolved_event, get_unsolved_events,
    extract_info_from_event_dict, get_finding_url,
    get_status_vulns_by_time_range, create_weekly_date, get_accepted_vulns,
    get_by_time_range, create_register_by_week, create_data_format_chart,
    get_first_week_dates, get_date_last_vulns,
    create_msj_finding_pending, format_vulnerabilities,
    get_project_indicators,
    integrates_delete_obsolete_orgs,
    calculate_vulnerabilities
)
from backend.utils import datetime as datetime_utils

from back import settings

from test_async.utils import create_dummy_simple_session

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
    test_data = get_finding_url(dumb_finding_dict)
    expected_output = 'https://integrates.fluidattacks.com/groups/test/test/description'
    assert test_data == expected_output

@freeze_time('2019-09-15')
async def test_calculate_vulnerabilities():
    finding_id = '436992569'
    assert await calculate_vulnerabilities(finding_id) == 17

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
    last_day = '2020-09-07 23:59:59'
    vuln = await get_vuln('80d6a69f-a376-46be-98cd-2fdedcffdcc0')
    test_data = get_by_time_range(
        vuln[0], last_day
    )
    expected_output = 1
    assert test_data == expected_output

async def test_create_register_by_week():
    project_name = 'unittesting'
    test_data = await create_register_by_week(project_name)
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
    expected_output = ('2018-09-24 00:00:00', '2018-09-30 23:59:59')
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
    not_new_treatment_finding = await get_finding('422286126')
    new_treatment_finding = await get_finding('436992569')

    test_data = await create_msj_finding_pending(not_new_treatment_finding)
    expected_output = ''
    assert test_data == expected_output

    test_data = await create_msj_finding_pending(new_treatment_finding)
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
    assert len(test_data) == 15
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
async def test_integrates_delete_obsolete_orgs():
    org_id = 'ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448'
    org_name = 'kiba'
    org_ids = []
    async for organization_id, _ in iterate_organizations():
        org_ids.append(organization_id)
    assert org_id in org_ids
    assert len(org_ids) == 8

    now_str = datetime_utils.get_as_str(
         datetime_utils.get_now()
    )
    await update_pending_deletion_date(
        org_id,
        org_name,
        now_str
    )
    await integrates_delete_obsolete_orgs()
    new_org_ids = []
    async for organization_id, _ in iterate_organizations():
        new_org_ids.append(organization_id)
    assert org_id not in new_org_ids
    assert len(new_org_ids) == 7

    org_id = 'ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de'
    org_pending_deletion_date = await get_pending_deletion_date_str(org_id)
    assert org_pending_deletion_date == '2020-01-29 19:00:00'
