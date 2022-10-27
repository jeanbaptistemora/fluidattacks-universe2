# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    LoadingStrategy,
)
from ._per_stream import (
    RecreatePerStream,
)
from ._recreate_all import (
    RecreateAll,
)
from dataclasses import (
    dataclass,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.sql_client import (
    SqlClient,
)
from redshift_client.table.client import (
    TableClient,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class Strategies:
    """namespace for supported strategies"""

    _client: SqlClient

    def recreate_all_schema(self, target: SchemaId) -> LoadingStrategy:
        _client = SchemaClient(self._client)
        """recreates and backup all target schema"""
        return RecreateAll(target, _client).strategy

    def recreate_per_stream(
        self, target: SchemaId, persistent_tables: FrozenSet[str]
    ) -> LoadingStrategy:
        """recreates and backups all non-persistent tables, appends data if persistent"""
        _client = SchemaClient(self._client)
        _client_2 = TableClient(self._client)
        return RecreatePerStream(
            target, _client, _client_2, persistent_tables
        ).strategy


__all__ = [
    "LoadingStrategy",
]
