from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    Query,
    SqlClient,
)
from typing import (
    Dict,
)


def init_table_2_query(client: SqlClient, table: TableId) -> Cmd[None]:
    statement = """
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
        """
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    return client.execute(
        Query.dynamic_query(statement, freeze(identifiers)), None
    )
