from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from purity.v2.adapters import (
    to_cmd,
)
from purity.v2.cmd import (
    Cmd,
)


def init_table_2_query(client: Client, table: TableID) -> Cmd[None]:
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
    return to_cmd(lambda: client.cursor.execute_query(query))
