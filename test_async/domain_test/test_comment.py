import pytest

from decimal import Decimal
from django.test import TestCase

import backend.domain.comment as comment_domain

pytestmark = [
    pytest.mark.asyncio,
]


class CommentTests(TestCase):

    async def test_list_comments(self):
        finding_id = '422286126'
        test_data = await comment_domain.get_comments(
            'unittesting', finding_id, 'integratesuser@gmail.com')
        expected_output = [{
            'parent': 0, 'created': '2019/08/20 16:35:16',
            'modified': '2019/08/20 16:35:16',
            'content': 'This is a comenting test',
            'email': 'unittest@fluidattacks.com',
            'fullname': 'Hacker at Fluid Attacks',
            'id': 1566336916294}]
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0] is not None
        assert sorted(test_data) == sorted(expected_output)

    @pytest.mark.changes_db
    def test_fill_comment_data(self):
        test_data = {
            'content': 'test content',
            'created': '2018-12-27 16:30:28',
            'email': 'unittesting@test.com',
            'user_id': Decimal('1582646735480'),
            'modified': '2020-02-25 11:05:35',
            'parent': Decimal('0')
        }
        res_data_no_fullname = \
            comment_domain.fill_comment_data('unittesting', 'customer', test_data)
        assert res_data_no_fullname['fullname'] == 'unittesting@test.com'

        test_data['fullname'] = ''
        res_data_empty_fullname = \
            comment_domain.fill_comment_data('unittesting', 'customer', test_data)

        assert res_data_empty_fullname['fullname'] == 'unittesting@test.com'
