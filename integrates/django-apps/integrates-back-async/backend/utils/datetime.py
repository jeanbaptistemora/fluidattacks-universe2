# pylint: disable=too-many-arguments
from datetime import datetime, timedelta
import pytz

from django.conf import settings
from django.utils.timezone import make_aware


TZN = pytz.timezone(settings.TIME_ZONE)
iso_format: str = '%Y-%m-%d %H:%M:%S'


def get_from_str(
        date_str: str, date_format: str = iso_format) -> datetime:
    unaware_datetime = datetime.strptime(date_str, date_format)
    return make_aware(unaware_datetime, TZN)


def get_as_str(date: datetime, date_format: str = iso_format) -> str:
    return date.strftime(date_format)


def get_now() -> datetime:
    return datetime.now(tz=TZN)


def get_plus_delta(
        date: datetime, days: int = 0, seconds: int = 0,
        microseconds: int = 0, milliseconds: int = 0, minutes: int = 0,
        hours: int = 0, weeks: int = 0) -> datetime:
    date_plus_delta = date + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_plus_delta


def get_now_plus_delta(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0) -> datetime:
    now = get_now()
    now_plus_delta = get_plus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_plus_delta


def get_minus_delta(
        date: datetime, days: int = 0, seconds: int = 0,
        microseconds: int = 0, milliseconds: int = 0, minutes: int = 0,
        hours: int = 0, weeks: int = 0) -> datetime:
    date_minus_delta = date - timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return date_minus_delta


def get_now_minus_delta(
        days: int = 0, seconds: int = 0, microseconds: int = 0,
        milliseconds: int = 0, minutes: int = 0, hours: int = 0,
        weeks: int = 0) -> datetime:
    now = get_now()
    now_minus_delta = get_minus_delta(
        now, days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )
    return now_minus_delta
