# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _encode,
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
from fa_purity.json.primitive import (
    Primitive,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from target_snowflake import (
    _assert,
)
from target_snowflake.db import (
    SchemaId,
)
from target_snowflake.schema import (
    TableId,
    TableObj,
)
from target_snowflake.sql_client import (
    Cursor,
    DatabaseId,
    Identifier,
    Query,
)
from target_snowflake.table import (
    ColumnId,
)
from typing import (
    Callable,
    Dict,
    FrozenSet,
    Tuple,
)


@dataclass(frozen=True)
class SchemaClient:
    _cursor: Cursor
    _db: DatabaseId
    _schema: SchemaId

    def new(
        self, table_obj: TableObj, if_not_exist: bool = False
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
            "database": self._db.db_name,
            "schema": self._schema.name,
            "table": table_obj.id_obj.name,
        }
        for index, cid in enum_primary_keys:
            identifiers[f"pkey_{index}"] = cid.name
        for index, cid in enum_columns:
            identifiers[f"name_{index}"] = cid.name
        values = {
            f"default_{index}": table_obj.table.columns[cid].default
            for index, cid in enum_columns
        }
        query = Query(stm, freeze(identifiers), freeze(values))
        return self._cursor.execute(query)

    def table_ids(self) -> Cmd[FrozenSet[TableId]]:
        _stm = (
            "SELECT tables.table_name FROM information_schema.tables",
            "WHERE table_schema = %(schema_name)s",
        )
        stm = " ".join(_stm)
        values: Dict[str, Primitive] = {
            "schema_name": self._schema.name.sql_identifier
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

    def create_like(
        self, blueprint: Tuple[SchemaId, TableId], new_table: TableId
    ) -> Cmd[None]:
        stm = """
            CREATE TABLE {new_schema}.{new_table} (
                LIKE {blueprint_schema}.{blueprint_table}
            )
        """
        identifiers: Dict[str, Identifier] = {
            "new_schema": self._schema.name,
            "new_table": new_table.name,
            "blueprint_schema": blueprint[0].name,
            "blueprint_table": blueprint[1].name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def exist(self, table_id: TableId) -> Cmd[bool]:
        stm = """
            SELECT EXISTS (
                SELECT * FROM information_schema.tables
                WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            );
        """
        args: Dict[str, Primitive] = {
            "table_schema": self._schema.name.sql_identifier,
            "table_name": table_id.name.sql_identifier,
        }
        query = Query(stm, freeze({}), freeze(args))
        return self._cursor.execute(query) + self._cursor.fetch_one().map(
            lambda m: m.map(
                lambda i: _assert.assert_bool(i.data[0]).unwrap()
            ).unwrap()
        )

    def rename(self, table_id: TableId, new_name: TableId) -> Cmd[None]:
        stm = """
            ALTER TABLE {schema}.{table} RENAME TO {new_name}
        """
        identifiers: Dict[str, Identifier] = {
            "schema": self._schema.name,
            "table": table_id.name,
            "new_name": new_name.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def _delete(self, table_id: TableId, cascade: bool) -> Cmd[None]:
        _cascade = "CASCADE" if cascade else ""
        stm = f"""
            DROP TABLE {{schema}}.{{table}} {_cascade}
        """
        identifiers: Dict[str, Identifier] = {
            "schema": self._schema.name,
            "table": table_id.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def delete(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, False)

    def delete_cascade(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, True)
