import pytest

from django.test import TestCase

from app.domain.finding import (
    list_comments, get_email_recipients, get_age_finding,
    get_tracking_vulnerabilities, get_findings)
from app.dal.vulnerability import get_vulnerabilities


@pytest.mark.usefixtures(
    'create_users_table',
    'create_projects_table',
    'create_project_access_table')
class FindingTests(TestCase):

    def test_list_comments(self):
        comment_type = 'comment'
        finding_id = '436992569'

        test_data = list_comments(comment_type, finding_id)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0] is not None

        comment_type = 'observation'
        test_data = list_comments(comment_type, finding_id)
        expected_output = [{
            'parent': 0, 'created': '2019/01/08 17:05:14',
            'modified': '2019/01/08 17:05:14',
            'email': u'test@test.com', 'content': u'Test comment',
            'fullname': u'Test User', 'id': 1546985114796}]
        assert test_data == expected_output

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
        expected_output = {'date': u'2019-01-17', 'effectiveness': 100,
                           'open': 0, 'closed': 1, 'cycle': 0}
        assert test_data[0] == expected_output

    def test_get_findings(self):
        finding_ids = ['436992569', '422286126']
        test_data = get_findings(finding_ids)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0]['findingId'] == '436992569'
