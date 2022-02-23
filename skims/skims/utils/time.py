from datetime import (
    datetime,
    timezone,
)
import pytz  # type: ignore

TIME_ZONE = "America/Bogota"
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DEFAULT_ISO_STR = "2000-01-01T05:00:00+00:00"
DEFAULT_STR = "2000-01-01 00:00:00"
TZ = pytz.timezone(TIME_ZONE)


def get_utc_timestamp() -> float:
    return datetime.now().timestamp()


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


def format_justification_date(date_string: str) -> str:
    just_date = get_datetime_from_iso_str(date_string)
    formatted_date = get_as_str(just_date, date_format="%Y/%m/%d %H:%M")
    return formatted_date


def get_datetime_from_iso_str(iso8601utc_str: str) -> datetime:
    iso8601utc = datetime.fromisoformat(iso8601utc_str)
    return get_from_str(get_as_str(iso8601utc))


def get_iso_date() -> str:
    return datetime.now(tz=timezone.utc).isoformat()
