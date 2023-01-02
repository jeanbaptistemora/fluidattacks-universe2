from ._core import (
    Client,
    Tables,
)
from ._delta_update import (
    CommitStampDiff,
)
from ._real_client import (
    RealClient,
)
from redshift_client.sql_client import (
    SqlClient,
)


def new_client(_sql_client: SqlClient) -> Client:
    return RealClient.new(_sql_client).client()


__all__ = [
    "Tables",
    "Client",
    "CommitStampDiff",
]
