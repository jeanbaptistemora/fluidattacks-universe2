from contextlib import (
    suppress,
)
from ntplib import (
    NTPClient,
    NTPException,
)
from typing import (
    Optional,
)


def get_offset() -> Optional[float]:
    with suppress(NTPException):
        response = NTPClient().request("pool.ntp.org", port=123, version=3)

        return response.offset

    return None
