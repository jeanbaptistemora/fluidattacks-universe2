# pylint: disable=too-many-arguments
from datetime import datetime, timedelta
import pytz

from django.conf import settings
from django.utils.timezone import make_aware


TZN = pytz.timezone(settings.TIME_ZONE)
iso_format: str = '%Y-%m-%d %H:%M:%S'


def get_str_as_datetime(
        date_str: str, date_format: str = iso_format) -> datetime:
    unaware_datetime = datetime.strptime(date_str, date_format)
    return make_aware(unaware_datetime, TZN)


def get_datetime_as_str(date: datetime, date_format: str = iso_format) -> str:
    return date.strftime(date_format)


def get_current_datetime() -> datetime:
    return datetime.now(tz=TZN)


def get_current_datetime_as_str(date_format: str = iso_format) -> str:
    now = get_current_datetime()
    return get_datetime_as_str(now, date_format=date_format)


def get_datetime_plus_delta(
        date: datetime, days: int = 0, seconds: int = 0,
        microseconds: int = 0, milliseconds: int = 0, minutes: int = 0,
        hours: int = 0, weeks: int = 0) -> datetime:
    date_plus_delta = date + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_plus_delta


def get_datetime_plus_delta_as_str(
        date: datetime, days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0, date_format: str = iso_format) -> str:
    date_plus_delta_as_str = get_datetime_as_str(
        get_datetime_plus_delta(
            date=date, days=days, seconds=seconds, microseconds=microseconds,
            milliseconds=milliseconds, minutes=minutes, hours=hours,
            weeks=weeks
        ),
        date_format=date_format
    )
    return date_plus_delta_as_str


def get_current_datetime_plus_delta(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0) -> datetime:
    now = get_current_datetime()
    now_plus_delta = get_datetime_plus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_plus_delta


def get_current_datetime_plus_delta_as_str(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0, date_format: str = iso_format) -> str:
    now = get_current_datetime()
    now_plus_delta_as_str = get_datetime_plus_delta_as_str(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks,
        date_format=date_format
    )
    return now_plus_delta_as_str


def get_datetime_minus_delta(
        date: datetime, days: int = 0, seconds: int = 0,
        microseconds: int = 0, milliseconds: int = 0, minutes: int = 0,
        hours: int = 0, weeks: int = 0) -> datetime:
    date_minus_delta = date - timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_minus_delta


def get_datetime_minus_delta_as_str(
        date: datetime, days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0, date_format: str = iso_format) -> str:
    date_minus_delta_as_str = get_datetime_as_str(
        get_datetime_minus_delta(
            date=date, days=days, seconds=seconds, microseconds=microseconds,
            milliseconds=milliseconds, minutes=minutes, hours=hours,
            weeks=weeks
        ),
        date_format=date_format
    )
    return date_minus_delta_as_str


def get_current_datetime_minus_delta(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0) -> datetime:
    now = get_current_datetime()
    now_minus_delta = get_datetime_minus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_minus_delta


def get_current_datetime_minus_delta_as_str(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0, date_format: str = iso_format) -> str:
    now = get_current_datetime()
    now_minus_delta_as_str = get_datetime_minus_delta_as_str(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks,
        date_format=date_format
    )
    return now_minus_delta_as_str
