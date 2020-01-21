import pytest

from django.test import TestCase

from datetime import datetime, timedelta
from backend.domain.finding import (
    get_age_finding,
    get_tracking_vulnerabilities, get_findings, update_treatment)
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
        values_accepted = {'justification': 'This is a test treatment justification',
                           'bts_url': '',
                           'treatment': 'ACCEPTED'}
        test_accepted = update_treatment(finding_id, values_accepted, 'unittesting@fluidattacks.com')
        assert test_accepted is True
        date = datetime.now() + timedelta(days=181)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        values_accepted_date_error = {'justification': 'This is a test treatment justification',
                                      'bts_url': '',
                                      'treatment': 'ACCEPTED',
                                      'acceptance_date': date}
        with pytest.raises(InvalidDate):
            assert update_treatment(finding_id, values_accepted_date_error, 'unittesting@fluidattacks.com')
        date_future = datetime.now() + timedelta(days=60)
        date_future = date_future.strftime('%Y/%m/%d %H:%M:%S')
        values_accepted_format_error = {'justification': 'This is a test treatment justification',
                                        'bts_url': '',
                                        'treatment': 'ACCEPTED',
                                        'acceptance_date': date_future}
        with pytest.raises(InvalidDateFormat):
            assert update_treatment(finding_id, values_accepted_format_error, 'unittesting@fluidattacks.com')
