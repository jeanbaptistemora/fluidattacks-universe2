# Standard library
from datetime import (
    datetime,
)


def get_utc_timestamp() -> float:
    return datetime.utcnow().timestamp()
