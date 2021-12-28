from code_etl.client.encoder import (
    CommitTableRow,
    RawRow,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
)
from dataclasses import (
    fields,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)


def all_data(table: TableID) -> Query:
    _attrs = ",".join([f.name for f in fields(RawRow)])
    args = SqlArgs(
        identifiers={
            "schema": table.schema.name,
            "table": table.table_name,
        }
    )
    return Query(f"SELECT {_attrs} FROM {{schema}}.{{table}}", args)


def all_data_count(table: TableID) -> Query:
    return Query(
        """
        SELECT COUNT(*) FROM {schema}.{table}
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )


def insert_row(table: TableID) -> Query:
    _fields = ",".join(tuple(f.name for f in fields(CommitTableRow)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(CommitTableRow)))
    return Query(
        f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values})",
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )


def insert_unique_row(table: TableID) -> Query:
    _fields = ",".join(tuple(f.name for f in fields(CommitTableRow)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(CommitTableRow)))
    return Query(
        f"""
        INSERT INTO {{schema}}.{{table}} ({_fields}) SELECT {values}
        WHERE NOT EXISTS (
            SELECT hash, namespace, repository
            FROM {{schema}}.{{table}}
            WHERE
                hash = %(hash)s
                and namespace = %(namespace)s
                and repository = %(repository)s
        )
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )


def update_users(table: TableID) -> Query:
    return Query(
        """
        UPDATE {schema}.{table}
        SET
            author_email = %(author_email)s,
            author_name = %(author_name)s,
            committer_email = %(committer_email)s,
            committer_name = %(committer_name)s
        WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )


def commit_exists(
    table: TableID,
    namespace: str,
    repo: str,
    commit_hash: str,
) -> Query:
    return Query(
        """
        SELECT hash, namespace, repository
        FROM {schema}.{table}
        WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
        """,
        SqlArgs(
            {
                "namespace": namespace,
                "repository": repo,
                "hash": commit_hash,
            },
            {
                "schema": table.schema.name,
                "table": table.table_name,
            },
        ),
    )


def last_commit_hash(table: TableID, namespace: str, repo: str) -> Query:
    return Query(
        """
        SELECT hash FROM {schema}.{table}
        WHERE
            hash != %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
        ORDER BY seen_at DESC, authored_at DESC
        LIMIT 1
        """,
        SqlArgs(
            {
                "namespace": namespace,
                "repository": repo,
                "hash": COMMIT_HASH_SENTINEL,
            },
            {
                "schema": table.schema.name,
                "table": table.table_name,
            },
        ),
    )
