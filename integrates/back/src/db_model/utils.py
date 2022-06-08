from datetime import (
    datetime,
    timedelta,
    timezone,
)


def get_date_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


def get_min_iso_date(date: datetime) -> datetime:
    return datetime.combine(
        date.astimezone(tz=timezone.utc),
        datetime.min.time(),
    )


def get_first_day_iso_date() -> str:
    now = get_min_iso_date(datetime.now(tz=timezone.utc))

    return (now - timedelta(days=(now.isoweekday() - 1) % 7)).isoformat()
