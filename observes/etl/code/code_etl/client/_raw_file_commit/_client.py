# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _encode,
)
from code_etl.client._raw_objs import (
    RawFileCommitRelation,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.frozen import (
    freeze,
)
import logging
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
    SqlClient,
)
from typing import (
    Dict,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class RawFileCommitClient:
    _private: _Private
    _sql_client: SqlClient
    _table: TableId

    def insert(self, rows: FrozenList[RawFileCommitRelation]) -> Cmd[None]:
        _fields = ",".join(RawFileCommitRelation.fields())
        values = ",".join(
            tuple(f"%({f})s" for f in RawFileCommitRelation.fields())
        )
        identifiers: Dict[str, str] = {
            "schema": self._table.schema.name,
            "table": self._table.name,
        }
        query = Query.dynamic_query(
            f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES ({values})",
            freeze(identifiers),
        )
        msg = Cmd.from_cmd(lambda: LOG.debug("inserting %s rows", len(rows)))
        return msg.bind(
            lambda _: self._sql_client.batch(
                query,
                tuple(QueryValues(_encode.primitive_encode(r)) for r in rows),
            )
        )
