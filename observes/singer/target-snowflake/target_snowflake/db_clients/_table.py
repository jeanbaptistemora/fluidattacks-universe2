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
from fa_purity.pure_iter.factory import (
    from_flist,
)
from target_snowflake.column import (
    ColumnId,
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
from target_snowflake.table import (
    TableObj,
)
from typing import (
    Callable,
    Dict,
)


@dataclass(frozen=True)
class TableClient:
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
