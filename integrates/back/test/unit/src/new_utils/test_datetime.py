from datetime import (
    datetime,
    timedelta,
)
from db_model.utils import (
    get_datetime_with_offset,
)
from freezegun import (
    freeze_time,
)
from newutils import (
    datetime as datetime_utils,
)
import pytz
from settings import (
    TIME_ZONE,
)

tzn = pytz.timezone(TIME_ZONE)


@freeze_time("2019-12-01")
def test_default_date() -> None:
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
def test_get_from_str() -> None:
    now = datetime_utils.get_now()
    now_str = datetime_utils.get_as_str(now)
    assert datetime_utils.get_from_str(now_str) == now


@freeze_time("2019-12-01")
def test_get_as_str() -> None:
    now = datetime_utils.get_now()
    assert datetime_utils.get_as_str(now) == "2019-11-30 19:00:00"


@freeze_time("2019-12-01")
def test_get_now() -> None:
    now = datetime.now(tz=tzn)
    assert datetime_utils.get_now() == now


@freeze_time("2019-12-01")
def test_get_plus_delta() -> None:
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1)
    assert (
        datetime_utils.get_plus_delta(now, days=1, minutes=1, seconds=1)
        == now + delta
    )


@freeze_time("2019-12-01")
def test_get_now_plus_delta() -> None:
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1, hours=1)
    assert (
        datetime_utils.get_now_plus_delta(
            days=1, minutes=1, seconds=1, hours=1
        )
        == now + delta
    )


@freeze_time("2019-12-01")
def test_get_minus_delta() -> None:
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1)
    assert (
        datetime_utils.get_minus_delta(now, days=1, minutes=1, seconds=1)
        == now - delta
    )


@freeze_time("2019-12-01")
def test_get_now_minus_delta() -> None:
    now = datetime_utils.get_now()
    delta = timedelta(days=1, minutes=1, seconds=1, hours=1)
    assert (
        datetime_utils.get_now_minus_delta(
            days=1, minutes=1, seconds=1, hours=1
        )
        == now - delta
    )


@freeze_time("2019-12-01")
def test_get_as_epoch() -> None:
    epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())

    assert epoch == 1575158400


@freeze_time("2019-12-01")
def test_get_from_epoch() -> None:
    now = datetime_utils.get_now()
    epoch = datetime_utils.get_as_epoch(now)
    epoch_date = datetime_utils.get_from_epoch(epoch)

    assert epoch_date == now


def test_get_date_with_offset() -> None:
    base_iso8601 = datetime.fromisoformat("2022-10-03T20:07:02.868165+00:00")
    assert get_datetime_with_offset(
        base_iso8601,
        datetime.fromisoformat("2022-10-03T20:07:02.868188+00:00"),
    ) == datetime.fromisoformat("2022-10-03T20:07:03.868165+00:00")
    assert get_datetime_with_offset(
        base_iso8601, datetime.fromisoformat("2022-10-03T20:07:01+00:00")
    ) == datetime.fromisoformat("2022-10-03T20:07:03.868165+00:00")
    assert get_datetime_with_offset(
        base_iso8601, datetime.fromisoformat("2022-10-03T20:07:59+00:00")
    ) == datetime.fromisoformat("2022-10-03T20:07:59+00:00")
    assert get_datetime_with_offset(
        base_iso8601,
        datetime.fromisoformat("2022-10-03T20:07:02.868165+00:00"),
        offset=10,
    ) == datetime.fromisoformat("2022-10-03T20:07:12.868165+00:00")
