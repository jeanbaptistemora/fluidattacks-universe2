import pytest
import time

from collections import namedtuple
from django.test import TestCase

from datetime import datetime, timedelta
from backend.domain.finding import (
    add_comment, get_age_finding, update_client_description,
    get_tracking_vulnerabilities, get_findings, update_treatment,
    handle_acceptation
)
from backend.mailer import get_email_recipients
from backend.dal.vulnerability import get_vulnerabilities
from backend.exceptions import (InvalidDateFormat, InvalidDate)


class FindingTests(TestCase):

    def test_get_email_recipients(self):
        comment_type = 'comment'
        finding_id = '436992569'

        test_data = get_email_recipients(comment_type, finding_id)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], str)

    def test_get_tracking_vulnerabilities(self):
        finding_id = '436992569'
        vulnerabilities = get_vulnerabilities(finding_id)
        test_data = get_tracking_vulnerabilities(vulnerabilities)
        expected_output = {'date': '2019-08-30', 'effectiveness': 0,
                           'open': 1, 'closed': 0, 'cycle': 0}
        assert test_data[0] == expected_output

    def test_get_findings(self):
        finding_ids = ['436992569', '422286126']
        test_data = get_findings(finding_ids)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0]['findingId'] == '436992569'

    def test_update_treatment(self):
        finding_id = '463461507'
        date = datetime.now() + timedelta(days=181)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        values_in_progress = {'justification': 'This is a test treatment justification',
                              'treatment': 'IN PROGRESS', 'acceptance_date': date}
        test_in_progress = update_treatment(finding_id, values_in_progress, 'integratesuser@gmail.com')
        assert test_in_progress is True
        vulns = get_vulnerabilities(finding_id)
        assert 'treatment_manager' in vulns[0]
        values_new = {'treatment': 'NEW'}
        test_new = update_treatment(finding_id, values_new, '')
        assert test_new is True
        vulns = get_vulnerabilities(finding_id)
        assert 'treatment_manager' not in vulns[0]
        assert 'treatment_manager' not in vulns[1]

    def test_update_client_description(self):
        Status = namedtuple('Status', 'bts_changed treatment_changed')
        update = Status(bts_changed=True, treatment_changed=True)
        finding_id = '463461507'
        values_accepted = {'justification': 'This is a test treatment justification',
                           'bts_url': '',
                           'treatment': 'ACCEPTED',
                           'acceptance_date': '-'}
        test_accepted = update_client_description(
            finding_id, values_accepted, 'unittesting@fluidattacks.com', update)
        assert test_accepted is True
        date = datetime.now() + timedelta(days=181)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        values_accepted_date_error = {'justification': 'This is a test treatment justification',
                                      'bts_url': '',
                                      'treatment': 'ACCEPTED',
                                      'acceptance_date': date}
        with pytest.raises(InvalidDate):
            assert update_client_description(
                finding_id, values_accepted_date_error, 'unittesting@fluidattacks.com', update)
        date_future = datetime.now() + timedelta(days=60)
        date_future = date_future.strftime('%Y/%m/%d %H:%M:%S')
        values_accepted_format_error = {'justification': 'This is a test treatment justification',
                                        'bts_url': '',
                                        'treatment': 'ACCEPTED',
                                        'acceptance_date': date_future}
        with pytest.raises(InvalidDateFormat):
            assert update_client_description(
                finding_id, values_accepted_format_error, 'unittesting@fluidattacks.com', update)

    def test_add_comment(self):
        finding_id = '463461507'
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'comment_type': 'comment',
            'user_id': comment_id,
            'content': 'Test comment',
            'created': current_time,
            'fullname': 'unittesting',
            'modified': current_time,
            'parent': '0'
        }
        assert add_comment('unittest@fluidattacks.com', comment_data, finding_id, False)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data['created'] = current_time
        comment_data['modified'] = current_time
        comment_data['parent'] = str(comment_id)
        assert add_comment('unittest@fluidattacks.com', comment_data, finding_id, False)

    def test_handle_acceptation(self):
        finding_id = '463461507'
        observations = 'Test observations'
        user_mail = 'unittest@fluidattacks.com'
        response = 'REJECTED'
        test_data = handle_acceptation(finding_id, observations, user_mail, response)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output
