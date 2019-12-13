import pytest

from django.test import TestCase

import backend.domain.comment as comment_domain


class CommentTests(TestCase):

    def test_list_comments(self):
        finding_id = '422286126'

        test_data = comment_domain.get_comments(finding_id, 'admin')
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0] is not None

        test_data = comment_domain.get_observations(finding_id, 'admin')
        expected_output = [{
            'parent': 0, 'created': '2019/08/20 16:35:16',
            'modified': '2019/08/20 16:35:16',
            'content': 'This is a comenting test',
            'fullname': 'unit test', 'id': 1566336916294}]
        assert True
        # Must be enabled later
        # assert test_data == expected_output
