from datetime import datetime, timedelta
import pytz
import pytest

from django.conf import settings
from django.test import TestCase
from backend.domain.user import (
    get_current_date,
)

class UserTests(TestCase):
    def test_get_current_date(self):
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today()
        date = today.strftime('%Y-%m-%d %H:%M')
        test_data = get_current_date()[:-3]
        assert isinstance(test_data, str)
        assert test_data == date
