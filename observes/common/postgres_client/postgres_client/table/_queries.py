# pylint: skip-file
# Standard libraries
from typing import (
    Dict,
    FrozenSet,
    List,
    Optional,
)

# Local libraries
from returns.maybe import Maybe
from postgres_client.cursor import (
    DynamicSQLargs,
    Query,
)
from postgres_client.table.common import MetaTable, TableID
from postgres_client.table.common.column import Column


class MutateColumnException(Exception):
    pass


class TableCreationFail(Exception):
    pass


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
            f"Columns: {diff_names.intersection(current_names)}"
        )
    queries: List[Query] = []
    for column in diff_columns:
        statement: str = (
            "ALTER TABLE {table_path} "
            "ADD COLUMN {column_name} "
            "{field_type} default %(default_val)s"
        )
        args = DynamicSQLargs(
            values={"default_val": column.default_val},
            identifiers={
                "table_path": table.path,
                "column_name": column.name,
                "field_type": column.field_type.value,
            },
        )
        query = Query.new(
            statement,
            Maybe.from_value(args),
        )
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
    args = DynamicSQLargs(
        values={
            "table_schema": table_id.schema,
            "table_name": table_id.table_name,
        }
    )
    return Query.new(
        statement,
        Maybe.from_value(args),
    )


def retrieve(table_id: TableID) -> Query:
    """Retrieve Table from DB"""
    statement = """
        SELECT ordinal_position AS position,
            column_name,
            data_type,
            CASE WHEN character_maximum_length IS not null
                    THEN character_maximum_length
                    ELSE numeric_precision end AS max_length,
            is_nullable,
            column_default AS default_value
        FROM information_schema.columns
        WHERE table_name = %(table_name)s
            AND table_schema = %(table_schema)s
        ORDER BY ordinal_position;
    """
    args = DynamicSQLargs(
        values={
            "table_schema": table_id.schema,
            "table_name": table_id.table_name,
        }
    )
    return Query.new(
        statement,
        Maybe.from_value(args),
    )


def create(table: MetaTable, if_not_exist: bool = False) -> Query:
    table_path: str = table.path
    pkeys_fields: str = ""
    if table.primary_keys:
        p_fields: str = ",".join(
            [f"{{pkey_{n}}}" for n in range(len(table.primary_keys))]
        )
        pkeys_fields = f",PRIMARY KEY({p_fields})"
    not_exists: str = "" if not if_not_exist else "IF NOT EXISTS "
    fields: str = ",".join(
        [f"{{name_{n}}} {{field_type_{n}}}" for n in range(len(table.columns))]
    )
    fields_def: str = f"{fields}{pkeys_fields}"
    statement: str = f"CREATE TABLE {not_exists}{{table_path}} ({fields_def})"
    identifiers: Dict[str, Optional[str]] = {"table_path": table_path}
    for index, value in enumerate(table.primary_keys):
        identifiers[f"pkey_{index}"] = value
    for index, column in enumerate(table.columns):
        identifiers[f"name_{index}"] = column.name
        identifiers[f"field_type_{index}"] = column.field_type.value

    args = DynamicSQLargs(identifiers=identifiers)
    return Query.new(statement, Maybe.from_value(args))


def create_like(blueprint: TableID, new_table: TableID) -> Query:
    query = """
        CREATE TABLE {new_schema}.{new_table} (
            LIKE {blueprint_schema}.{blueprint_table}
        );
    """
    identifiers: Dict[str, Optional[str]] = {
        "new_schema": new_table.schema,
        "new_table": new_table.table_name,
        "blueprint_schema": blueprint.schema,
        "blueprint_table": blueprint.table_name,
    }
    args = DynamicSQLargs(identifiers=identifiers)
    return Query.new(query, Maybe.from_value(args))


def rename(table: TableID, new_name: str) -> Query:
    query = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name};
    """
    identifiers: Dict[str, Optional[str]] = {
        "schema": table.schema,
        "table": table.table_name,
        "new_name": new_name,
    }
    args = DynamicSQLargs(identifiers=identifiers)
    return Query.new(query, Maybe.from_value(args))


def delete(table: TableID) -> Query:
    query = """
        DROP TABLE {schema}.{table} CASCADE;
    """
    identifiers: Dict[str, Optional[str]] = {
        "schema": table.schema,
        "table": table.table_name,
    }
    args = DynamicSQLargs(identifiers=identifiers)
    return Query.new(query, Maybe.from_value(args))


def move(
    source: TableID,
    target: TableID,
) -> List[Query]:
    query = """
        ALTER TABLE {target_schema}.{target_table}
        APPEND FROM {source_schema}.{source_table};
    """
    identifiers: Dict[str, Optional[str]] = {
        "source_schema": source.schema,
        "source_table": source.table_name,
        "target_schema": target.schema,
        "target_table": target.table_name,
    }
    args = DynamicSQLargs(identifiers=identifiers)
    return [Query.new(query, Maybe.from_value(args)), delete(source)]
