# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _encode,
)
from ._rows_package import (
    RowsPackage,
)
from .db import (
    DbManager,
    UpperMethods as DbUpperMethods,
)
from .table import (
    ColumnId,
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
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.pure_iter.transform import (
    chain,
    consume,
)
from target_snowflake import (
    _assert,
)
from target_snowflake.snowflake_client.db import (
    DbTableId,
    SchemaId,
)
from target_snowflake.snowflake_client.schema import (
    TableId,
    TableObj,
)
from target_snowflake.snowflake_client.sql_client import (
    Cursor,
    DatabaseId,
    Identifier,
    Primitive,
    Query,
)
from target_snowflake.snowflake_client.table import (
    Table,
)
from typing import (
    Callable,
    Dict,
    FrozenSet,
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

    # Db manager
    def exist_schema(self, schema: FullSchemaPointer) -> Cmd[bool]:
        stm = "SHOW SCHEMAS IN DATABASE {database}"
        identifiers: Dict[str, Identifier] = {"database": schema.db.db_name}
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query) + self._cursor.fetch_all().map(
            lambda i: tuple(
                Identifier.from_raw(r.data[1].to_str().unwrap()) for r in i
            )
        ).map(lambda l: schema.schema.name in l)

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
        stm: str = "DROP SCHEMA {database}.{schema}" + opt
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
    def create_table(
        self,
        schema: FullSchemaPointer,
        table_obj: TableObj,
        if_not_exist: bool = False,
    ) -> Cmd[None]:
        enum_primary_keys = from_flist(
            tuple(enumerate(table_obj.table.primary_keys))
        )
        enum_columns = from_flist(tuple(enumerate(table_obj.table.order)))
        p_fields = ",".join(
            enum_primary_keys.map(lambda t: f"{{pkey_{t[0]}}}")
        )
        pkeys_template = (
            f",PRIMARY KEY({p_fields})" if table_obj.table.primary_keys else ""
        )
        not_exists = "" if not if_not_exist else "IF NOT EXISTS"
        encode_nullable: Callable[[bool], str] = (
            lambda b: "NULL" if b else "NOT NULL"
        )

        def _encode_field(index: int, column_id: ColumnId) -> str:
            column = table_obj.table.columns[column_id]
            return f"""
                {{name_{index}}} {_encode.encode_type(column.data_type)}
                DEFAULT %(default_{index})s {encode_nullable(column.nullable)}
            """

        fields_template: str = ",".join(
            enum_columns.map(lambda t: _encode_field(*t))
        )
        stm = f"CREATE TABLE {not_exists} {{database}}.{{schema}}.{{table}} ({fields_template}{pkeys_template})"
        identifiers: Dict[str, Identifier] = {
            "database": schema.db.db_name,
            "schema": schema.schema.name,
            "table": table_obj.id_obj.name,
        }
        for index, cid in enum_primary_keys:
            identifiers[f"pkey_{index}"] = cid.name
        for index, cid in enum_columns:
            identifiers[f"name_{index}"] = cid.name
        values: Dict[str, Primitive] = {
            f"default_{index}": table_obj.table.columns[cid].default
            for index, cid in enum_columns
        }
        query = Query(stm, freeze(identifiers), freeze(values))
        return self._cursor.execute(query)

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

    def insert(
        self,
        table_id: FullTablePointer,
        table_def: Table,
        items: RowsPackage,
    ) -> Cmd[None]:
        enum_fields = from_flist(tuple(enumerate(table_def.order)))
        _fields = ",".join(enum_fields.map(lambda t: f"{{field_{t[0]}}}"))
        values_placeholders = (
            items.rows.enumerate(1)
            .map(
                lambda t: ",".join(
                    from_range(range(1, items.row_length + 1)).map(
                        lambda r: f"%(value_{t[0]}_{r})s"
                    )
                )
            )
            .map(lambda p: f"({p})")
        )
        values_placeholder = ",".join(values_placeholders)
        stm = f"""
            INSERT INTO {{db}}.{{schema}}.{{table}} ({_fields}) VALUES {values_placeholder}
        """
        identifiers: Dict[str, Identifier] = {
            "db": table_id.db.db_name,
            "schema": table_id.schema.name,
            "table": table_id.table.name,
        }
        values: Dict[str, Primitive] = (
            items.rows.enumerate(1)
            .map(
                lambda t: from_flist(t[1].data)
                .enumerate(1)
                .map(lambda i: (f"value_{t[0]}_{i[0]}", i[1]))
            )
            .transform(lambda x: dict(chain(x)))
        )
        for i, c in enumerate(table_def.order):
            identifiers[f"field_{i}"] = c.name
        query = Query(stm, freeze(identifiers), freeze(values))
        return items.rows.map(lambda d: self._cursor.execute(query)).transform(
            consume
        )

    def append_table(
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

    def table_ids(self, schema: FullSchemaPointer) -> Cmd[FrozenSet[TableId]]:
        _stm = (
            "SELECT tables.table_name FROM information_schema.tables",
            "WHERE table_catalog = %(database)s AND table_schema = %(schema)s",
        )
        stm = " ".join(_stm)
        values: Dict[str, Primitive] = {
            "database": Primitive(schema.db.db_name.sql_identifier),
            "schema": Primitive(schema.schema.name.sql_identifier),
        }
        query = Query(stm, freeze({}), freeze(values))
        return self._cursor.execute(query) + self._cursor.fetch_all().map(
            lambda x: from_flist(x)
        ).map(
            lambda p: p.map(lambda r: to_primitive(r.data[0], str).unwrap())
            .map(Identifier.from_raw)
            .map(TableId)
            .transform(lambda x: frozenset(x))
        )

    def exist_table(self, table: FullTablePointer) -> Cmd[bool]:
        stm = """
            SELECT EXISTS (
                SELECT * FROM information_schema.tables
                WHERE table_catalog = %(database)s
                AND table_schema = %(schema)s
                AND table_name = %(table)s
            );
        """
        args: Dict[str, Primitive] = {
            "database": Primitive(table.db.db_name.sql_identifier),
            "schema": Primitive(table.schema.name.sql_identifier),
            "table": Primitive(table.table.name.sql_identifier),
        }
        query = Query(stm, freeze({}), freeze(args))
        return self._cursor.execute(query) + self._cursor.fetch_one().map(
            lambda m: m.map(
                lambda i: _assert.assert_bool(i.data[0]).unwrap()
            ).unwrap()
        )

    def delete_table(
        self, table: FullTablePointer, cascade: bool
    ) -> Cmd[None]:
        _cascade = "CASCADE" if cascade else ""
        stm = f"""
            DROP TABLE {{database}}.{{schema}}.{{table}} {_cascade}
        """
        identifiers: Dict[str, Identifier] = {
            "database": table.db.db_name,
            "schema": table.schema.name,
            "table": table.table.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    # managers
    def db_manager(self, database: DatabaseId) -> DbManager:
        def _schema_path(schema: SchemaId) -> FullSchemaPointer:
            return FullSchemaPointer(database, schema)

        def _table_path(schema: DbTableId) -> FullTablePointer:
            return FullTablePointer(database, schema.schema, schema.table)

        class _ConcreteDbMethods(DbUpperMethods):
            def rename_schema(s, old: SchemaId, new: SchemaId) -> Cmd[None]:
                return self.rename_schema(_schema_path(old), _schema_path(new))

            def delete_schema(s, target: SchemaId, cascade: bool) -> Cmd[None]:
                return self.delete_schema(_schema_path(target), cascade)

            def create_schema(
                s, schema: SchemaId, if_not_exist: bool = False
            ) -> Cmd[None]:
                return self.create_schema(_schema_path(schema), if_not_exist)

            def exist_schema(s, schema: SchemaId) -> Cmd[bool]:
                return self.exist_schema(_schema_path(schema))

            def create_table(
                s, table_id: DbTableId, table: Table, if_not_exist: bool
            ) -> Cmd[None]:
                _schema = _schema_path(table_id.schema)
                _table_obj = TableObj(table_id.table, table)
                return self.create_table(_schema, _table_obj, if_not_exist)

            def create_table_like(
                s, blueprint: DbTableId, new_table: DbTableId
            ) -> Cmd[None]:
                return self.create_table_like(
                    _table_path(blueprint), _table_path(new_table)
                )

            def rename_table(s, old: DbTableId, new: DbTableId) -> Cmd[None]:
                return self.move_table(_table_path(old), _table_path(new))

            def delete_table(s, target: DbTableId, cascade: bool) -> Cmd[None]:
                return self.delete_table(_table_path(target), cascade)

            def table_ids(s, schema: SchemaId) -> Cmd[FrozenSet[TableId]]:
                return self.table_ids(_schema_path(schema))

            def append_table(
                s, source: DbTableId, target: DbTableId
            ) -> Cmd[None]:
                return self.append_table(
                    _table_path(source), _table_path(target)
                )

            def insert(
                s,
                table_id: DbTableId,
                table_def: Table,
                items: RowsPackage,
            ) -> Cmd[None]:
                return self.insert(_table_path(table_id), table_def, items)

        return DbManager(self._cursor, _ConcreteDbMethods())
