# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from code_etl.client.db_client import (
    DbClient,
)
from fa_purity.cmd import (
    Cmd,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)


def init_table_2_query(client: DbClient, table: TableID) -> Cmd[None]:
    query = Query(
        """
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            author_email VARCHAR(256),
            author_name VARCHAR(256),
            authored_at TIMESTAMPTZ,
            committer_email VARCHAR(256),
            committer_name VARCHAR(256),
            committed_at TIMESTAMPTZ,
            hash CHAR(40),
            fa_hash CHAR(64),
            message VARCHAR(4096),
            summary VARCHAR(256),
            total_insertions INTEGER,
            total_deletions INTEGER,
            total_lines INTEGER,
            total_files INTEGER,

            namespace VARCHAR(64),
            repository VARCHAR(4096),
            seen_at TIMESTAMPTZ,

            PRIMARY KEY (
                namespace,
                repository,
                hash
            )
        ) SORTKEY (namespace, repository)
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            },
        ),
    )
    return client.execute_query(query)
