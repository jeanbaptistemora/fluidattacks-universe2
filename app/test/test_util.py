import os
from datetime import datetime

from django.test import TestCase

from app.dal.finding import get_finding
from app.util import (
    response, is_name, is_numeric, ord_asc_by_criticidad, user_email_filter,
    assert_file_mime, has_release, get_last_vuln, validate_release_date,
    validate_future_releases)


class UtilTests(TestCase):

    def test_response(self):
        data = 'this is data'
        message = 'this is a test'
        error = '500'
        test_data = response(data, message, error)
        expected_output = {
            'message': 'this is a test',
            'data': 'this is data',
            'error': '500'}
        print type(test_data)

    def test_is_name(self):
        bad_names = ['', 'asd>;', 'asd asd']
        good_names = ['name', 'name1234']
        for name in bad_names:
            assert not is_name(name)
        for name in good_names:
            assert is_name(name)

    def test_is_numeric(self):
        bad_inputs = ['', '123a', 'aaaa', '123>']
        good_input = '123123'
        for data in bad_inputs:
            assert not is_numeric(data)
        assert is_numeric(good_input)

    def test_ord_asc_by_criticidad(self):
        sortable_data = [
            {'severityCvss': 40}, {'severityCvss': 13}, {'severityCvss': 20},
            {'severityCvss': 30}, {'severityCvss': 12}, {'severityCvss': 1},
            {'severityCvss': 54}
        ]
        test_data = ord_asc_by_criticidad(sortable_data)
        expected_output = [
            {'severityCvss': 54}, {'severityCvss': 40}, {'severityCvss': 30},
            {'severityCvss': 20}, {'severityCvss': 13}, {'severityCvss': 12},
            {'severityCvss': 1}]
        assert test_data == expected_output

    def test_user_email_filter(self):
        emails = ['test@test.com', 'test@fluidattacks.com', 'test2@test.test']
        fluid_user = 'test@fluidattacks.com'
        external_user = 'test@external.com'
        
        test_data = user_email_filter(emails, fluid_user)
        expected_output = emails
        assert test_data == expected_output

        test_data = user_email_filter(emails, external_user)
        expected_output = ['test@test.com', 'test2@test.test']
        assert test_data == expected_output

    def test_assert_file_mime(self):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, 'mock/test-vulns.yaml')
        non_included_filename = os.path.join(path, 'mock/test.7z')
        allowed_mimes = ['text/plain']
        assert assert_file_mime(filename, allowed_mimes)
        assert not assert_file_mime(non_included_filename, allowed_mimes)

    def test_has_release(self):
        test_dict = {'releaseDate': 'date'}
        test_dict_with_no_release_date = {'noReleaseDate': 'date'}
        assert has_release(test_dict)
        assert not has_release(test_dict_with_no_release_date)

    def test_get_last_vuln(self):
        finding = get_finding('422286126')
        test_data = get_last_vuln(finding)
        expected_output = datetime(2018, 7, 9).date()
        assert test_data == expected_output

    def test_validate_release_date(self):
        finding = get_finding('422286126')
        assert validate_release_date(finding)

    def test_validate_future_releases(self):
        finding_released = get_finding('475041513')
        assert not validate_future_releases(finding_released)
