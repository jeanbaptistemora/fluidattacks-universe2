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
    RowData,
)
from target_snowflake.table import (
    Table,
)
from typing import (
    Dict,
    Optional,
    Tuple,
)


@dataclass(frozen=True)
class TableClient:
    _cursor: Cursor
    _db: DatabaseId
    _schema: SchemaId
    _table_id: TableId
    _local_def: Optional[Table]

    def insert(
        self,
        table_def: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        enum_fields = from_flist(tuple(enumerate(table_def.order)))
        _fields = ",".join(enum_fields.map(lambda t: f"{{field_{t[0]}}}"))
        values_placeholder = ",".join(enum_fields.map(lambda _: "?"))
        stm = f"""
            INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values_placeholder})
        """
        identifiers: Dict[str, Identifier] = {
            "schema": self._schema.name,
            "table": self._table_id.name,
        }
        for i, c in enumerate(table_def.order):
            identifiers[f"field_{i}"] = c.name
        query = Query(stm, freeze(identifiers), freeze({}))
        return (
            items.chunked(limit)
            .map(lambda p: self._cursor.execute_many(query, p))
            .transform(consume)
        )

    def insert_from(self, source: Tuple[SchemaId, TableId]) -> Cmd[None]:
        """
        This method copies data from source to target.
        Both tables must exists and share the same table definition.
        """
        stm = """
            INSERT INTO {target_schema}.{target_table}
            SELECT * FROM {source_schema}.{source_table};
        """
        identifiers: Dict[str, Identifier] = {
            "source_schema": source[0].name,
            "source_table": source[1].name,
            "target_schema": self._schema.name,
            "target_table": self._table_id.name,
        }
        query = Query(stm, freeze(identifiers), freeze({}))
        return self._cursor.execute(query)
