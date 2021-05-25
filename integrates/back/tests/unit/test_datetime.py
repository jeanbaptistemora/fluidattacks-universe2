import pytz
import pytest
from datetime import datetime, timedelta

from freezegun import freeze_time

from newutils import datetime as datetime_utils
from settings import TIME_ZONE


tzn = pytz.timezone(TIME_ZONE)


@freeze_time("2019-12-01")
def test_default_date():
    default_date = datetime_utils.get_from_str(datetime_utils.DEFAULT_STR)
    assert datetime_utils.DEFAULT_STR == datetime_utils.get_as_str(
        default_date
    )
    delta = timedelta(days=1, minutes=1, seconds=1, microseconds=1)
    assert (
        datetime_utils.get_plus_delta(
            default_date, days=1, minutes=1, seconds=1, microseconds=1
        )
        == default_date + delta
    )
    assert (
        datetime_utils.get_minus_delta(
            default_date, days=1, minutes=1, seconds=1, microseconds=1
        )
        == default_date - delta
    )


@freeze_time("2019-12-01")
def test_get_from_str():
    now = datetime_utils.get_now()
    now_str = datetime_utils.get_as_str(now)
    assert datetime_utils.get_from_str(now_str) == now


@freeze_time("2019-12-01")
def test_get_as_str():
    now = datetime_utils.get_now()
    assert datetime_utils.get_as_str(now) == "2019-11-30 19:00:00"


@freeze_time("2019-12-01")
def test_get_now():
    now = datetime.now(tz=tzn)
    assert datetime_utils.get_now() == now


@freeze_time("2019-12-01")
def test_get_plus_delta():
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1)
    assert (
        datetime_utils.get_plus_delta(now, days=1, minutes=1, seconds=1)
        == now + delta
    )


@freeze_time("2019-12-01")
def test_get_now_plus_delta():
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1, hours=1)
    assert (
        datetime_utils.get_now_plus_delta(
            days=1, minutes=1, seconds=1, hours=1
        )
        == now + delta
    )


@freeze_time("2019-12-01")
def test_get_minus_delta():
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1)
    assert (
        datetime_utils.get_minus_delta(now, days=1, minutes=1, seconds=1)
        == now - delta
    )


@freeze_time("2019-12-01")
def test_get_now_minus_delta():
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1, hours=1)
    assert (
        datetime_utils.get_now_minus_delta(
            days=1, minutes=1, seconds=1, hours=1
        )
        == now - delta
    )


@freeze_time("2019-12-01")
def test_get_as_epoch():
    epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())

    assert epoch == 1575158400


@freeze_time("2019-12-01")
def test_get_from_epoch():
    now = datetime_utils.get_now()
    epoch = datetime_utils.get_as_epoch(now)
    epoch_date = datetime_utils.get_from_epoch(epoch)

    assert epoch_date == now
