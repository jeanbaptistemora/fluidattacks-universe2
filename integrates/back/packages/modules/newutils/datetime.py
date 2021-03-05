# pylint: disable=too-many-arguments
from datetime import datetime, timedelta

import pytz

from back import settings


DEFAULT_STR = '2000-01-01 00:00:00'
TZN = pytz.timezone(settings.TIME_ZONE)
iso_format: str = '%Y-%m-%d %H:%M:%S'


def get_from_str(
    date_str: str,
    date_format: str = iso_format,
    timezone: str = settings.TIME_ZONE,
) -> datetime:
    unaware_datetime = datetime.strptime(date_str, date_format)
    return pytz.timezone(timezone).localize(unaware_datetime, is_dst=False)


def get_as_str(
    date: datetime,
    date_format: str = iso_format,
) -> str:
    return date.strftime(date_format)


def get_now(timezone: str = settings.TIME_ZONE) -> datetime:
    return datetime.now(tz=pytz.timezone(timezone))


def get_utc_timestamp() -> float:
    return datetime.now().timestamp()


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
    days: float = 0,
    seconds: float = 0,
    microseconds: float = 0,
    milliseconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
    timezone: str = settings.TIME_ZONE,
) -> datetime:
    now = get_now(timezone=timezone)
    now_plus_delta = get_plus_delta(
        now,
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
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
    days: float = 0,
    seconds: float = 0,
    microseconds: float = 0,
    milliseconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
    timezone: str = settings.TIME_ZONE,
) -> datetime:
    now = get_now(timezone=timezone)
    now_minus_delta = get_minus_delta(
        now,
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
    )
    return now_minus_delta


def get_from_epoch(epoch: int) -> datetime:
    date = datetime.fromtimestamp(epoch, TZN)

    return date


def get_as_epoch(date: datetime) -> int:
    epoch = int(date.timestamp())

    return epoch
