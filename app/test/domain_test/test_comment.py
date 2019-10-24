import pytest

from django.test import TestCase

import app.domain.comment as comment_domain


class CommentTests(TestCase):

    def test_list_comments(self):
        finding_id = '436992569'

        test_data = comment_domain.get_comments(finding_id)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0] is not None

        test_data = comment_domain.get_observations(finding_id)
        expected_output = [{
            'parent': 0, 'created': '2019/01/08 17:05:14',
            'modified': '2019/01/08 17:05:14',
            'email': 'test@test.com', 'content': 'Test comment',
            'fullname': 'Test User', 'id': 1546985114796}]
        assert test_data == expected_output
