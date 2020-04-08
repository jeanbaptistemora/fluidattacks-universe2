# -*- coding: utf-8 -*-
import pytest
from collections import OrderedDict
from decimal import Decimal

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from jose import jwt

from backend.dal.finding import get_finding
from backend.domain.project import get_released_findings
from backend.dal.vulnerability import get_vulnerabilities
from backend.scheduler import (
    is_not_a_fluidattacks_email, remove_fluid_from_recipients,
    is_a_unsolved_event, get_unsolved_events,
    extract_info_from_event_dict, get_finding_url,
    get_status_vulns_by_time_range, create_weekly_date, get_accepted_vulns,
    get_by_time_range, create_register_by_week, create_data_format_chart,
    get_all_vulns_by_project, get_first_week_dates, get_date_last_vulns,
    create_msj_finding_pending, all_users_formatted, format_vulnerabilities,
    get_project_indicators
)


class SchedulerTests(TestCase):

    def test_is_not_a_fluid_attacks_email(self):
        fluid_attacks_email = 'test@fluidattacks.com'
        not_fluid_attacks_email = 'test@test.com'
        assert is_not_a_fluidattacks_email(not_fluid_attacks_email)
        assert not is_not_a_fluidattacks_email(fluid_attacks_email)

    def test_remove_fluid_from_recipients(self):
        emails = [
            'test@fluidattacks.com', 'test2@fluidattacks.com', 'test@test.com',
            'test2@test.com'
        ]
        test_data = remove_fluid_from_recipients(emails)
        expected_output = ['test@test.com', 'test2@test.com']
        assert test_data == expected_output

    def test_is_a_unsolved_event(self):
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

    def test_get_unsolved_events(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        project_name = 'unittesting'
        test_data = get_unsolved_events(project_name)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert [ev for ev in test_data if ev['event_id'] == '540462628']

    def test_extract_info_from_event_dict(self):
        dumb_event_dict = {
            'id': 'testid', 'event_type': 'test', 'detail': 'detail'
        }
        test_data = extract_info_from_event_dict(dumb_event_dict)
        expected_output = {'type': 'test', 'details': 'detail'}
        assert test_data == expected_output

    def test_get_finding_url(self):
        dumb_finding_dict = {'project_name': 'test', 'finding_id': 'test'}
        test_data = get_finding_url(dumb_finding_dict)
        expected_output = 'https://fluidattacks.com/integrates/dashboard#!\
/project/test/test/description'
        assert test_data == expected_output

    def test_get_status_vulns_by_time_range(self):
        released_findings = get_released_findings('UNITTESTING')
        first_day = '2019-01-01 12:00:00'
        last_day = '2019-06-30 23:59:59'
        vulns = get_all_vulns_by_project(released_findings)
        test_data = get_status_vulns_by_time_range(
            vulns, first_day, last_day, released_findings
        )
        expected_output = {'found': 8, 'accepted': 4, 'closed': 2}
        assert test_data == expected_output

    def test_create_weekly_date(self):
        first_date = '2019-09-19 13:23:32'
        test_data = create_weekly_date(first_date)
        expected_output = 'Sep 16 - 22, 2019'
        assert test_data == expected_output

    def test_get_accepted_vulns(self):
        released_findings = get_released_findings('UNITTESTING')
        first_day = '2019-01-01 12:00:00'
        last_day = '2019-06-30 23:59:59'
        vulns = get_all_vulns_by_project(released_findings)
        test_data = get_accepted_vulns(
            released_findings, vulns, first_day, last_day
        )
        expected_output = 4
        assert test_data == expected_output

    def test_get_by_time_range(self):
        finding = get_finding('422286126')
        first_day = '2019-01-01 12:00:00'
        last_day = '2019-06-30 23:59:59'
        vuln = get_vulnerabilities('422286126')[0]
        test_data = get_by_time_range(
            finding, vuln, first_day, last_day
        )
        expected_output = 1
        assert test_data == expected_output

    def test_create_register_by_week(self):
        project_name = 'unittesting'
        test_data = create_register_by_week(project_name)
        assert isinstance(test_data, list)
        for item in test_data:
            assert isinstance(item, list)
            assert isinstance(item[0], dict)
            assert item[0] is not None

    def test_create_data_format_chart(self):
        registers = OrderedDict(
            [('Sep 24 - 30, 2018',
              {'found': 2, 'accepted': 0, 'closed': 0, 'assumed_closed': 0})]
        )
        test_data = create_data_format_chart(registers)
        expected_output = [
            [{'y': 2, 'x': 'Sep 24 - 30, 2018'}],
            [{'y': 0, 'x': 'Sep 24 - 30, 2018'}],
            [{'y': 0, 'x': 'Sep 24 - 30, 2018'}],
            [{'y': 0, 'x': 'Sep 24 - 30, 2018'}]
        ]
        assert test_data == expected_output

    def test_get_all_vulns_by_project(self):
        all_registers = get_released_findings('UNITTESTING')
        test_data = get_all_vulns_by_project(all_registers)
        assert isinstance(test_data, list)
        for item in test_data:
            assert isinstance(item, dict)
        assert test_data[0]['finding_id']

    def test_get_first_week_dates(self):
        vulns = get_vulnerabilities('422286126')
        test_data = get_first_week_dates(vulns)
        expected_output = ('2018-09-24 00:00:00', '2018-09-30 23:59:59')
        assert test_data == expected_output

    def test_get_date_last_vulns(self):
        vulns = get_vulnerabilities('422286126')
        test_data = get_date_last_vulns(vulns)
        expected_output = '2019-01-07 16:01:26'
        assert test_data == expected_output

    def test_format_vulnerabilities(self):
        act_finding = get_finding('422286126')
        positive_delta = 1
        neutral_delta = 0
        negative_delta = -1

        test_data = format_vulnerabilities(positive_delta, act_finding)
        expected_output = 'FIN.S.0051. Weak passwords reversed (+1)'
        assert test_data == expected_output

        test_data = format_vulnerabilities(neutral_delta, act_finding)
        expected_output = ''
        assert test_data == expected_output

        test_data = format_vulnerabilities(negative_delta, act_finding)
        expected_output = 'FIN.S.0051. Weak passwords reversed (-1)'
        assert test_data == expected_output

    def test_create_msj_finding_pending(self):
        not_new_treatment_finding = get_finding('422286126')
        new_treatment_finding = get_finding('436992569')

        test_data = create_msj_finding_pending(not_new_treatment_finding)
        expected_output = ''
        assert test_data == expected_output

        test_data = create_msj_finding_pending(new_treatment_finding)
        expected_output = u'FIN.S.0038. Fuga de información de negocio'
        assert expected_output in test_data

    def test_all_user_formatted(self):
        company = '_test_'
        test_data = all_users_formatted(company)
        expected_output = {company: 0}
        assert test_data == expected_output

    def test_get_project_indicators(self):
        project_name = 'unittesting'
        test_data = get_project_indicators(project_name)
        assert isinstance(test_data, dict)
        assert len(test_data) == 5
        assert test_data['max_open_severity'] == Decimal(6.3).quantize(Decimal('0.1'))
