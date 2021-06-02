# The purpose of this module is to return datetime AWARE objects
# so the entire codebase work in UTC-based clocks no matter the data-source
from datetime import (
    datetime,
    timedelta,
    timezone,
)

INTEGRATES_1: str = "%Y-%m-%d %H:%M:%S"


def from_colombian(string: str, fmt: str) -> datetime:
    naive = datetime.strptime(string, fmt)
    aware = naive.replace(tzinfo=timezone(offset=timedelta(hours=-5.0)))
    return aware
