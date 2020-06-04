from datetime import datetime, timedelta
import pytz
import pytest

from django.conf import settings
from django.test import TestCase
from backend.domain.user import (
    get_all_companies,
    get_all_inactive_users,
    get_all_users_report,
    logging_users_report,
    get_current_date,
)

class UserTests(TestCase):

    def test_get_all_companies(self):
        all_expected_companies = ['FLUID', 'UNITTEST']
        all_companies = sorted(get_all_companies())
        assert all_companies == all_expected_companies

    def test_get_all_inactive_users(self):
        test_1 = get_all_inactive_users('2000-10-10 12:00:00')
        test_2 = get_all_inactive_users('2020-12-24 23:59:59')
        expected_emails_1 = ['unittest2']
        expected_emails_2 = ['unittest2', 'unittest3']
        assert expected_emails_1 == sorted(test_1)
        assert expected_emails_2 == sorted(test_2)

    def test_get_all_users_report(self):
        finish_date = \
            (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
        users = get_all_users_report('FLUID', finish_date)
        assert users >= 1

    def test_logging_users_report(self):
        # test_# = [excluded_company, init_date, finish_date]
        test_1 = ['fluid', '2018-05-03', '2020-01-01']
        test_2 = ['unittest', '2018-01-01', '2019-12-23']
        assert logging_users_report(*test_1) == 0
        assert logging_users_report(*test_2) == 3

    def test_get_current_date(self):
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today()
        date = today.strftime('%Y-%m-%d %H:%M')
        test_data = get_current_date()[:-3]
        assert isinstance(test_data, str)
        assert test_data == date
