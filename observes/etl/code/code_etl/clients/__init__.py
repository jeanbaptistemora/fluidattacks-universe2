from ._dry_client import (
    DryRunClient,
)
from ._real_client import (
    RealClient,
)
from code_etl.client import (
    Client,
)
from redshift_client.sql_client import (
    SqlClient,
)


def new_client(_sql_client: SqlClient) -> Client:
    return RealClient.new(_sql_client).client()


def dry_client(_sql_client: SqlClient) -> Client:
    return DryRunClient(RealClient.new(_sql_client)).client()
