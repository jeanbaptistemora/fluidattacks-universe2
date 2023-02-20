from contextlib import (
    suppress,
)
from ntplib import (
    NTPClient,
    NTPException,
)


def get_offset() -> float | None:
    with suppress(NTPException):
        response = NTPClient().request("pool.ntp.org", port=123, version=3)

        return response.offset

    return None
