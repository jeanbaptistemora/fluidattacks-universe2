# pylint: skip-file

import logging
from postgres_client.column import (
    Column,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from postgres_client.table._objs import (
    MetaTable,
)
from typing import (
    Dict,
    FrozenSet,
    List,
    Optional,
)


class MutateColumnException(Exception):
    pass


class TableCreationFail(Exception):
    pass


LOG = logging.getLogger(__name__)


def add_columns(
    table: MetaTable,
    columns: FrozenSet[Column],
) -> List[Query]:
    old_columns = table.columns
    new_columns = columns
    diff_columns: FrozenSet[Column] = new_columns - old_columns
    diff_names: FrozenSet[str] = frozenset(col.name for col in diff_columns)
    current_names: FrozenSet[str] = frozenset(col.name for col in old_columns)
    if not diff_names.isdisjoint(current_names):
        raise MutateColumnException(
            "Cannot update the type of existing columns."
            f"diff: {diff_columns}"
        )
    queries: List[Query] = []
    for column in diff_columns:
        field_type = column.c_type.field_type.value
        statement: str = (
            "ALTER TABLE {table_schema}.{table_name} "
            "ADD COLUMN {column_name} "
            f"{field_type} default %(default_val)s"
        )
        args = SqlArgs(
            values={"default_val": column.c_type.default_val},
            identifiers={
                "table_schema": str(table.table_id.schema),
                "table_name": str(table.table_id.table_name),
                "column_name": column.name,
            },
        )
        query = Query(statement, args)
        queries.append(query)
    return queries


def exist(table_id: TableID) -> Query:
    """Check existence of a Table on the DB"""
    statement = """
        SELECT EXISTS (
            SELECT * FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    args = SqlArgs(
        values={
            "table_schema": str(table_id.schema),
            "table_name": table_id.table_name,
        }
    )
    return Query(statement, args)


def retrieve(table_id: TableID) -> Query:
    """Retrieve Table from DB"""
    statement = """
        SELECT ordinal_position AS position,
            column_name,
            data_type,
            CASE WHEN character_maximum_length IS not null
                    THEN character_maximum_length
                    ELSE numeric_precision end AS max_length,
            numeric_scale,
            column_default AS default_value,
            is_nullable
        FROM information_schema.columns
        WHERE table_name = %(table_name)s
            AND table_schema = %(table_schema)s
        ORDER BY ordinal_position;
    """
    args = SqlArgs(
        values={
            "table_schema": str(table_id.schema),
            "table_name": table_id.table_name,
        }
    )
    return Query(statement, args)


def create(table: MetaTable, if_not_exist: bool = False) -> Query:
    table_path: str = "{schema}.{table_name}"
    pkeys_fields: str = ""
    if table.primary_keys:
        p_fields: str = ",".join(
            [f"{{pkey_{n}}}" for n in range(len(table.primary_keys))]
        )
        pkeys_fields = f",PRIMARY KEY({p_fields})"
    not_exists: str = "" if not if_not_exist else "IF NOT EXISTS "
    fields: str = ",".join(
        [
            f"{{name_{n}}} {column.c_type.field_type.value}"
            for n, column in enumerate(table.columns)
        ]
    )
    fields_def: str = f"{fields}{pkeys_fields}"
    statement: str = f"CREATE TABLE {not_exists}{table_path} ({fields_def})"
    identifiers: Dict[str, Optional[str]] = {
        "schema": str(table.table_id.schema),
        "table_name": table.table_id.table_name,
    }
    for index, value in enumerate(table.primary_keys):
        identifiers[f"pkey_{index}"] = value
    for index, column in enumerate(table.columns):
        identifiers[f"name_{index}"] = column.name

    args = SqlArgs(identifiers=identifiers)
    return Query(statement, args)


def create_like(blueprint: TableID, new_table: TableID) -> Query:
    query = """
        CREATE TABLE {new_schema}.{new_table} (
            LIKE {blueprint_schema}.{blueprint_table}
        );
    """
    identifiers: Dict[str, Optional[str]] = {
        "new_schema": str(new_table.schema),
        "new_table": new_table.table_name,
        "blueprint_schema": str(blueprint.schema),
        "blueprint_table": blueprint.table_name,
    }
    args = SqlArgs(identifiers=identifiers)
    return Query(query, args)


def rename(table: TableID, new_name: str) -> Query:
    query = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name};
    """
    identifiers: Dict[str, Optional[str]] = {
        "schema": str(table.schema),
        "table": table.table_name,
        "new_name": new_name,
    }
    args = SqlArgs(identifiers=identifiers)
    return Query(query, args)


def delete(table: TableID) -> Query:
    query = """
        DROP TABLE {schema}.{table} CASCADE;
    """
    identifiers: Dict[str, Optional[str]] = {
        "schema": str(table.schema),
        "table": table.table_name,
    }
    args = SqlArgs(identifiers=identifiers)
    return Query(query, args)


def redshift_move(
    source: TableID,
    target: TableID,
) -> List[Query]:
    query = """
        ALTER TABLE {target_schema}.{target_table}
        APPEND FROM {source_schema}.{source_table};
    """
    identifiers: Dict[str, Optional[str]] = {
        "source_schema": str(source.schema),
        "source_table": source.table_name,
        "target_schema": str(target.schema),
        "target_table": target.table_name,
    }
    args = SqlArgs(identifiers=identifiers)
    return [Query(query, args), delete(source)]


def move(
    source: TableID,
    target: TableID,
) -> List[Query]:
    """redshift_move equivalent for postgres DB"""
    query = """
        ALTER TABLE {source_schema}.{source_table}
        SET SCHEMA {target_schema};
    """
    identifiers: Dict[str, Optional[str]] = {
        "source_schema": str(source.schema),
        "source_table": source.table_name,
        "target_schema": str(target.schema),
    }
    args = SqlArgs(identifiers=identifiers)
    return [delete(target), Query(query, args)]
