from code_etl.client.encoder import (
    CommitTableRow,
    RawRow,
)
from code_etl.objs import (
    RepoId,
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
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.maybe import (
    Maybe,
)
from typing import (
    Optional,
)


def _all_data(table: TableID, namespace: Optional[str]) -> Query:
    _namespace = Maybe.from_optional(namespace)
    _attrs = ",".join([f.name for f in fields(RawRow)])
    args = SqlArgs(
        {"namespace": namespace} if namespace else {},
        {
            "schema": table.schema.name,
            "table": table.table_name,
        },
    )
    base_query = f"SELECT {_attrs} FROM {{schema}}.{{table}}"
    _query = _namespace.map(
        lambda _: f"{base_query} WHERE namespace = %(namespace)s"
    ).value_or(base_query)
    return Query(_query, args)


def namespace_data(table: TableID, namespace: str) -> Query:
    return _all_data(table, namespace)


def all_data(table: TableID) -> Query:
    return _all_data(table, None)


def all_data_count(table: TableID, namespace: Optional[str] = None) -> Query:
    _namespace = Maybe.from_optional(namespace)
    base_query = "SELECT COUNT(*) FROM {schema}.{table}"
    _query = _namespace.map(
        lambda _: f"{base_query} WHERE namespace = %(namespace)s"
    ).value_or(base_query)
    return Query(
        _query,
        SqlArgs(
            {"namespace": namespace} if namespace else {},
            {
                "schema": table.schema.name,
                "table": table.table_name,
            },
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
    repo: RepoId,
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
                "namespace": repo.namespace,
                "repository": repo.repository,
                "hash": commit_hash,
            },
            {
                "schema": table.schema.name,
                "table": table.table_name,
            },
        ),
    )


def last_commit_hash(table: TableID, repo: RepoId) -> Query:
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
                "namespace": repo.namespace,
                "repository": repo.repository,
                "hash": COMMIT_HASH_SENTINEL,
            },
            {
                "schema": table.schema.name,
                "table": table.table_name,
            },
        ),
    )


def update_row(
    table: TableID, row: CommitTableRow, _fields: FrozenList[str]
) -> Query:
    values = ",".join(tuple(f"{f} = %({f})s" for f in _fields))
    statement = f"""
        UPDATE {{schema}}.{{table}} SET {values} WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
    """
    args = SqlArgs(
        row.__dict__,
        {
            "schema": table.schema.name,
            "table": table.table_name,
        },
    )
    return Query(statement, args)
