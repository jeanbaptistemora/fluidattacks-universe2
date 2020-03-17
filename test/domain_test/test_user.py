from datetime import datetime, timedelta
import pytest
from django.test import TestCase
from backend.domain.user import get_all_users_report

class UserTests(TestCase):

    def test_get_all_users_report(self):
        finish_date = \
            (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
        users = get_all_users_report('FLUID', finish_date)
        assert users >= 1
