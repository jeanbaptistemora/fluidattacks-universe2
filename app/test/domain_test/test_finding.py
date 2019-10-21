import pytest

from django.test import TestCase

from datetime import datetime, timedelta
from app.domain.finding import (
    get_email_recipients, get_age_finding,
    get_tracking_vulnerabilities, get_findings, update_treatment)
from app.dal.vulnerability import get_vulnerabilities
from app.exceptions import (InvalidDateFormat, InvalidDate)


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
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
        expected_output = {'date': '2019-01-17', 'effectiveness': 100,
                           'open': 0, 'closed': 1, 'cycle': 0}
        assert test_data[0] == expected_output

    def test_get_findings(self):
        finding_ids = ['436992569', '422286126']
        test_data = get_findings(finding_ids)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0]['findingId'] == '436992569'

    def test_update_treatment(self):
        finding_id = '463461507'
        values_accepted = {'treatment_justification': 'This is a test treatment justification',
                           'treatment_manager': 'test@testmail.com',
                           'bts_url': '',
                           'treatment': 'ACCEPTED',
                           'acceptance_date': '2020-03-31 11:43:00'}
        test_accepted = update_treatment(finding_id, values_accepted)
        assert test_accepted is True
        date = datetime.now() + timedelta(days=181)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        values_accepted_date_error = {'treatment_justification': 'This is a test treatment justification',
                                      'treatment_manager': 'test@testmail.com',
                                      'bts_url': '',
                                      'treatment': 'ACCEPTED',
                                      'acceptance_date': date}
        with pytest.raises(InvalidDate):
            assert update_treatment(finding_id, values_accepted_date_error)
        date_future = datetime.now() + timedelta(days=60)
        date_future = date_future.strftime('%Y/%m/%d %H:%M:%S')
        values_accepted_format_error = {'treatment_justification': 'This is a test treatment justification',
                                 'treatment_manager': 'test@testmail.com',
                                 'bts_url': '',
                                 'treatment': 'ACCEPTED',
                                 'acceptance_date': date_future}
        with pytest.raises(InvalidDateFormat):
            assert update_treatment(finding_id, values_accepted_format_error)
