# pylint: disable=too-many-arguments
from datetime import datetime, timedelta
import pytz

from django.conf import settings
from django.utils.timezone import make_aware


TZN = pytz.timezone(settings.TIME_ZONE)
iso_format: str = '%Y-%m-%d %H:%M:%S'


def get_from_str(
        date_str: str, date_format: str = iso_format) -> datetime:
    if date_str == '0001-01-01 00:00:00':
        date_str = '1970-01-01 00:00:00'
    unaware_datetime = datetime.strptime(date_str, date_format)
    return make_aware(unaware_datetime, TZN, is_dst=False)


def get_as_str(date: datetime, date_format: str = iso_format) -> str:
    return date.strftime(date_format)


def get_now() -> datetime:
    return datetime.now(tz=TZN)


def get_plus_delta(
        date: datetime, days: float = 0, seconds: float = 0,
        microseconds: float = 0, milliseconds: float = 0, minutes: float = 0,
        hours: float = 0, weeks: float = 0) -> datetime:
    date_plus_delta = date + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_plus_delta


def get_now_plus_delta(
        days: float = 0, seconds: float = 0, microseconds: float = 0,
        milliseconds: float = 0, minutes: float = 0, hours: float = 0,
        weeks: float = 0) -> datetime:
    now = get_now()
    now_plus_delta = get_plus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_plus_delta


def get_minus_delta(
        date: datetime, days: float = 0, seconds: float = 0,
        microseconds: float = 0, milliseconds: float = 0, minutes: float = 0,
        hours: float = 0, weeks: float = 0) -> datetime:
    date_minus_delta = date - timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_minus_delta


def get_now_minus_delta(
        days: float = 0, seconds: float = 0, microseconds: float = 0,
        milliseconds: float = 0, minutes: float = 0, hours: float = 0,
        weeks: float = 0) -> datetime:
    now = get_now()
    now_minus_delta = get_minus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_minus_delta
