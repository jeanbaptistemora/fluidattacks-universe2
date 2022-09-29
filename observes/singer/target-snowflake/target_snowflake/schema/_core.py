# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)
from target_snowflake.sql_client import (
    Identifier,
)
from target_snowflake.table import (
    Table,
)


@dataclass(frozen=True)
class TableId:
    name: Identifier


@dataclass(frozen=True)
class TableObj:
    id_obj: TableId
    table: Table


@dataclass(frozen=True)
class Schema:
    tables: FrozenDict[TableId, Table]
