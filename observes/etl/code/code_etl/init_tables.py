from code_etl import (
    _utils,
)
from code_etl.client import (
    Tables,
)
from code_etl.clients import (
    new_client as code_client,
)
from fa_purity import (
    Cmd,
)
import logging
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
)

LOG = logging.getLogger(__name__)


def init_tables(
    db_id: DatabaseId, creds: Credentials, table: Tables
) -> Cmd[None]:
    # pylint: disable=too-many-arguments
    new_connection = connect(
        db_id,
        creds,
        False,
        IsolationLvl.READ_COMMITTED,
    )

    def _main(connection: DbConnection) -> Cmd[None]:
        client = new_client(connection, LOG).map(code_client)
        return client.bind(lambda c: c.init_table(table)) + connection.commit()

    return _utils.wrap_connection(new_connection, _main)
