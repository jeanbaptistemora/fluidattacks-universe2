# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.primitive import (
    Primitive,
)
from target_snowflake import (
    _assert,
)
from target_snowflake.schema import (
    SchemaId,
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
class DbClient:
    _cursor: Cursor
    _db: DatabaseId

    def exist(self, schema: SchemaId) -> Cmd[bool]:
        _stm = (
            "SELECT EXISTS",
            "(SELECT 1 FROM pg_namespace",
            "WHERE nspname = %(schema_name)s)",
        )
        stm = " ".join(_stm)
        values: Dict[str, Primitive] = {
            "schema_name": schema.name.sql_identifier
        }
        query = Query(stm, freeze({}), freeze(values))
        return self._cursor.execute(query) + self._cursor.fetch_one().map(
            lambda x: x.unwrap()
        ).map(lambda i: _assert.assert_bool(i.data[0]).unwrap())

    def _delete(self, schema: SchemaId, cascade: bool) -> Cmd[None]:
        opt = " CASCADE" if cascade else ""
        stm: str = "DROP SCHEMA {schema_name}" + opt
        identifiers: Dict[str, Identifier] = {"schema_name": schema.name}
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def delete(self, schema: SchemaId) -> Cmd[None]:
        return self._delete(schema, False)

    def delete_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._delete(schema, True)

    def rename(self, old: SchemaId, new: SchemaId) -> Cmd[None]:
        stm = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
        identifiers: Dict[str, Identifier] = {
            "from_schema": old.name,
            "schema_name": new.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def create(
        self, schema: SchemaId, if_not_exist: bool = False
    ) -> Cmd[None]:
        not_exist = " IF NOT EXISTS " if if_not_exist else ""
        stm = f"CREATE SCHEMA {not_exist} {{schema}}"
        identifiers: Dict[str, Identifier] = {"schema": schema.name}
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)

    def _recreate(self, schema: SchemaId, cascade: bool) -> Cmd[None]:
        nothing = Cmd.from_cmd(lambda: None)
        return self.exist(schema).bind(
            lambda b: self._delete(schema, cascade) if b else nothing
        ) + self.create(schema)

    def recreate(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, False)

    def recreate_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, True)
