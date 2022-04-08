from datetime import (
    datetime,
)
from os import (
    environ,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)

COMMIT_HASH_SENTINEL: str = "-" * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()

DB_ID = DatabaseId(
    environ["REDSHIFT_DATABASE"],
    environ["REDSHIFT_HOST"],
    int(environ["REDSHIFT_PORT"]),
)
DB_CREDS = Credentials(
    environ["REDSHIFT_USER"],
    environ["REDSHIFT_PASSWORD"],
)
