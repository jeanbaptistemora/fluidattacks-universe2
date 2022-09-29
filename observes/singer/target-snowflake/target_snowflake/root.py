# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from .db import (
    DbClient,
    UpperMethods as DbUpperMethods,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from target_snowflake.db import (
    SchemaId,
)
from target_snowflake.schema import (
    TableId,
)
from target_snowflake.sql_client import (
    Cursor,
    DatabaseId,
    Identifier,
    Query,
)
from typing import (
    Dict,
)


@dataclass(frozen=True)
class FullSchemaPointer:
    db: DatabaseId
    schema: SchemaId


@dataclass(frozen=True)
class FullTablePointer:
    db: DatabaseId
    schema: SchemaId
    table: TableId


@dataclass(frozen=True)
class RootManager:
    _cursor: Cursor

    def db_client(self, database: DatabaseId) -> DbClient:
        class _ConcreteDbMethods(DbUpperMethods):
            def rename_schema(s, old: SchemaId, new: SchemaId) -> Cmd[None]:
                _old = FullSchemaPointer(database, old)
                _new = FullSchemaPointer(database, new)
                return self.rename_schema(_old, _new)

            def delete_schema(s, target: SchemaId, cascade: bool) -> Cmd[None]:
                _target = FullSchemaPointer(database, target)
                return self.delete_schema(_target, cascade)

            def create_schema(
                s, schema: SchemaId, if_not_exist: bool = False
            ) -> Cmd[None]:
                _schema = FullSchemaPointer(database, schema)
                return self.create_schema(_schema, if_not_exist)

        return DbClient(self._cursor, _ConcreteDbMethods())

    # Db manager
    def create_schema(
        self, schema: FullSchemaPointer, if_not_exist: bool = False
    ) -> Cmd[None]:
        not_exist = " IF NOT EXISTS " if if_not_exist else ""
        stm = f"CREATE SCHEMA {not_exist} {{database}}.{{schema}}"
        identifiers: Dict[str, Identifier] = {
            "database": schema.db.db_name,
            "schema": schema.schema.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def delete_schema(
        self, schema: FullSchemaPointer, cascade: bool
    ) -> Cmd[None]:
        opt = " CASCADE" if cascade else ""
        stm: str = "DROP SCHEMA {database}.{schema_name}" + opt
        identifiers: Dict[str, Identifier] = {
            "database": schema.db.db_name,
            "schema": schema.schema.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def rename_schema(
        self, old: FullSchemaPointer, new: FullSchemaPointer
    ) -> Cmd[None]:
        stm = "ALTER SCHEMA {from_database}.{from_schema} RENAME TO {to_database}.{to_schema}"
        identifiers: Dict[str, Identifier] = {
            "from_database": old.db.db_name,
            "from_schema": old.schema.name,
            "to_database": new.db.db_name,
            "to_schema": new.schema.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    # Schema manager
    def move_table(
        self,
        source: FullTablePointer,
        target: FullTablePointer,
    ) -> Cmd[None]:
        stm = """
            ALTER TABLE {source_database}.{source_schema}.{source_table}
            RENAME TO {target_database}.{target_schema}.{target_table}
        """
        identifiers: Dict[str, Identifier] = {
            "source_database": source.db.db_name,
            "source_schema": source.schema.name,
            "source_table": source.table.name,
            "target_database": target.db.db_name,
            "target_schema": target.schema.name,
            "target_table": target.table.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def insert_from(
        self, source: FullTablePointer, target: FullTablePointer
    ) -> Cmd[None]:
        """
        This method copies data from source to target.
        Both tables must exists and share the same table definition.
        """
        stm = """
            INSERT INTO {target_db}.{target_schema}.{target_table}
            SELECT * FROM {source_db}.{source_schema}.{source_table};
        """
        identifiers: Dict[str, Identifier] = {
            "source_db": source.db.db_name,
            "source_schema": source.schema.name,
            "source_table": source.schema.name,
            "target_db": target.db.db_name,
            "target_schema": target.schema.name,
            "target_table": target.schema.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def create_table_like(
        self, blueprint: FullTablePointer, new_table: FullTablePointer
    ) -> Cmd[None]:
        stm = """
            CREATE TABLE {new_db}.{new_schema}.{new_table} (
                LIKE {blueprint_db}.{blueprint_schema}.{blueprint_table}
            )
        """
        identifiers: Dict[str, Identifier] = {
            "new_db": new_table.db.db_name,
            "new_schema": new_table.schema.name,
            "new_table": new_table.table.name,
            "blueprint_db": blueprint.db.db_name,
            "blueprint_schema": blueprint.schema.name,
            "blueprint_table": blueprint.table.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)
