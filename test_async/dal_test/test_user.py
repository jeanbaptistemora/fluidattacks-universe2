import pytest

from boto3.dynamodb.conditions import Attr, Key, Not
from django.test import TestCase
from backend.dal.user import (
    delete, get
)

class UserTests(TestCase):

    @pytest.mark.changes_db
    def test_delete(self):
        test_1 = 'unittest3'
        assert {
             'company' : 'unittest', 'date_joined': '2017-12-28 23:54:55',
             'last_login': '2019-10-29 13:40:37', 'email' : 'unittest3',
             'legal_remember' : True, 'registered' : False
          } == get(test_1)
        assert delete(test_1)
        assert {} == get(test_1)
