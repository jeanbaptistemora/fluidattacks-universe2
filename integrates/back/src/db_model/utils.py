from datetime import (
    datetime,
    timezone,
)


def get_date_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).replace(microsecond=0).isoformat()
