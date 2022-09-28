# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from target_snowflake.schema import (
    SchemaId,
)
from target_snowflake.sql_client import (
    Cursor,
    DatabaseId,
    Identifier,
    Query,
    RowData,
)
from target_snowflake.table import (
    TableObj,
)
from typing import (
    Dict,
)


@dataclass(frozen=True)
class TableOperations:
    _cursor: Cursor
    _db: DatabaseId
    _schema: SchemaId
    _table: TableObj

    def insert(
        self,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        enum_fields = from_flist(tuple(enumerate(self._table.table.order)))
        _fields = ",".join(enum_fields.map(lambda t: f"{{field_{t[0]}}}"))
        values_placeholder = ",".join(enum_fields.map(lambda _: "?"))
        stm = f"""
            INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values_placeholder})
        """
        identifiers: Dict[str, Identifier] = {
            "schema": self._schema.name,
            "table": self._table.id_obj.name,
        }
        for i, c in enumerate(self._table.table.order):
            identifiers[f"field_{i}"] = c.name
        query = Query(stm, freeze(identifiers), freeze({}))
        return (
            items.chunked(limit)
            .map(lambda p: self._cursor.execute_many(query, p))
            .transform(consume)
        )
