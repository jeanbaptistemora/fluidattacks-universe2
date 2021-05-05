# Third party libraries
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)
from typing import (
    Optional,
)
from ntplib import (
    NTPClient,
    NTPException,
)


def get_ntp_now() -> Optional[float]:
    with suppress(NTPException):
        response = NTPClient().request("pool.ntp.org", port=123, version=3)

        # System time
        timestamp = datetime.fromtimestamp(response.tx_time).timestamp()

        return timestamp

    return None
