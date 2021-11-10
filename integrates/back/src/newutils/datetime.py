# pylint: disable=too-many-arguments
from datetime import (
    date as datetype,
    datetime,
    timedelta,
    timezone,
)
import pytz  # type: ignore
from settings import (
    TIME_ZONE,
)

DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DEFAULT_ISO_STR = "2000-01-01T05:00:00+00:00"
DEFAULT_STR = "2000-01-01 00:00:00"
TZ = pytz.timezone(TIME_ZONE)


def as_zone(
    date: datetime,
    zone: str = TIME_ZONE,
) -> datetime:
    return date.astimezone(tz=pytz.timezone(zone))


def format_comment_date(date_string: str) -> str:
    comment_date = get_from_str(date_string)
    formatted_date = get_as_str(comment_date, date_format="%Y/%m/%d %H:%M:%S")
    return formatted_date


def get_from_str(
    date_str: str,
    date_format: str = DEFAULT_DATE_FORMAT,
    zone: str = TIME_ZONE,
) -> datetime:
    unaware_datetime = datetime.strptime(date_str, date_format)
    return pytz.timezone(zone).localize(unaware_datetime, is_dst=False)


def get_as_str(
    date: datetime,
    date_format: str = DEFAULT_DATE_FORMAT,
    zone: str = TIME_ZONE,
) -> str:
    return date.astimezone(tz=pytz.timezone(zone)).strftime(date_format)


def get_now(zone: str = TIME_ZONE) -> datetime:
    return datetime.now(tz=pytz.timezone(zone))


def get_now_as_str(zone: str = TIME_ZONE) -> str:
    return get_as_str(get_now(zone))


def get_utc_timestamp() -> float:
    return datetime.now().timestamp()


def get_plus_delta(
    date: datetime,
    days: float = 0,
    seconds: float = 0,
    microseconds: float = 0,
    milliseconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
) -> datetime:
    date_plus_delta = date + timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
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
    zone: str = TIME_ZONE,
) -> datetime:
    now = get_now(zone=zone)
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
    date: datetime,
    days: float = 0,
    seconds: float = 0,
    microseconds: float = 0,
    milliseconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
) -> datetime:
    date_minus_delta = date - timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
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
    zone: str = TIME_ZONE,
) -> datetime:
    now = get_now(zone=zone)
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
    date = datetime.fromtimestamp(epoch, TZ)

    return date


def get_as_epoch(date: datetime) -> int:
    epoch = int(date.timestamp())

    return epoch


def get_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


def get_iso_date() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def is_valid_format(date_str: str) -> bool:
    try:
        get_from_str(date_str)
        resp = True
    except ValueError:
        resp = False
    return resp


def get_date_from_iso_str(iso8601utc_str: str) -> datetype:
    iso8601utc = datetime.fromisoformat(iso8601utc_str)
    return get_from_str(get_as_str(iso8601utc)).date()
