# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from code_etl import (
    utils,
)
from code_etl.client import (
    Client,
    Tables,
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
        client = new_client(connection, LOG).map(Client.new)
        return client.bind(lambda c: c.init_table(table)) + connection.commit()

    return new_connection.bind(lambda c: utils.wrap_connection(c, _main))
