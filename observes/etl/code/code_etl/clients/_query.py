from ._raw_objs import (
    RawCommitStamp,
)
from code_etl._utils import (
    COMMIT_HASH_SENTINEL,
)
from code_etl.objs import (
    RepoId,
)
from fa_purity.frozen import (
    freeze,
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    Dict,
    Optional,
    Tuple,
)


def _all_data(
    table: TableId, namespace: Optional[str]
) -> Tuple[Query, QueryValues]:
    _namespace = Maybe.from_optional(namespace)
    _attrs = ",".join(RawCommitStamp.fields())
    base_stm = f"SELECT {_attrs} FROM {{schema}}.{{table}}"
    id_args: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    args: Dict[str, PrimitiveVal] = (
        {"namespace": namespace} if namespace else {}
    )
    stm = _namespace.map(
        lambda _: f"{base_stm} WHERE namespace = %(namespace)s"
    ).value_or(base_stm)
    return (
        Query.dynamic_query(stm, freeze(id_args)),
        QueryValues(freeze(args)),
    )


def namespace_data(
    table: TableId, namespace: str
) -> Tuple[Query, QueryValues]:
    return _all_data(table, namespace)


def all_data(table: TableId) -> Tuple[Query, QueryValues]:
    return _all_data(table, None)


def all_data_count(
    table: TableId, namespace: Optional[str] = None
) -> Tuple[Query, QueryValues]:
    _namespace = Maybe.from_optional(namespace)
    base_stm = "SELECT COUNT(*) FROM {schema}.{table}"
    stm = _namespace.map(
        lambda _: f"{base_stm} WHERE namespace = %(namespace)s"
    ).value_or(base_stm)
    args: Dict[str, PrimitiveVal] = (
        {"namespace": namespace} if namespace else {}
    )
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    return (
        Query.dynamic_query(stm, freeze(identifiers)),
        QueryValues(freeze(args)),
    )


def insert_row(table: TableId) -> Query:
    _fields = ",".join(RawCommitStamp.fields())
    values = ",".join(tuple(f"%({f})s" for f in RawCommitStamp.fields()))
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    return Query.dynamic_query(
        f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values})",
        freeze(identifiers),
    )


def insert_unique_row(table: TableId) -> Query:
    _fields = ",".join(RawCommitStamp.fields())
    values = ",".join(tuple(f"%({f})s" for f in RawCommitStamp.fields()))
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    return Query.dynamic_query(
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
        freeze(identifiers),
    )


def commit_exists(
    table: TableId,
    repo: RepoId,
    commit_hash: str,
) -> Tuple[Query, QueryValues]:
    statement = """
    SELECT 1
    FROM {schema}.{table}
    WHERE
        hash = %(hash)s
        and namespace = %(namespace)s
        and repository = %(repository)s
    """
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    args: Dict[str, PrimitiveVal] = {
        "namespace": repo.namespace,
        "repository": repo.repository,
        "hash": commit_hash,
    }
    return (
        Query.dynamic_query(statement, freeze(identifiers)),
        QueryValues(freeze(args)),
    )


def last_commit_hash(
    table: TableId, repo: RepoId
) -> Tuple[Query, QueryValues]:
    statement = """
    SELECT hash FROM {schema}.{table}
    WHERE
        hash != %(hash)s
        and namespace = %(namespace)s
        and repository = %(repository)s
    ORDER BY seen_at DESC, authored_at DESC
    LIMIT 1
    """
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    args: Dict[str, PrimitiveVal] = {
        "namespace": repo.namespace,
        "repository": repo.repository,
        "hash": COMMIT_HASH_SENTINEL,
    }
    return (
        Query.dynamic_query(statement, freeze(identifiers)),
        QueryValues(freeze(args)),
    )


def update_row(table: TableId, _fields: FrozenList[str]) -> Query:
    values = ",".join(tuple(f"{f} = %({f})s" for f in _fields))
    statement = f"""
        UPDATE {{schema}}.{{table}} SET {values} WHERE
            hash = %(hash)s
            and namespace = %(namespace)s
            and repository = %(repository)s
    """
    identifiers: Dict[str, str] = {
        "schema": table.schema.name,
        "table": table.name,
    }
    return Query.dynamic_query(statement, freeze(identifiers))
