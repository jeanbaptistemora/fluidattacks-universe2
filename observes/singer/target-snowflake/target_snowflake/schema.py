# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from .table import (
    Table,
    TableId,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)
from target_snowflake.sql_client import (
    Identifier,
)


@dataclass(frozen=True)
class SchemaId:
    name: Identifier


@dataclass(frozen=True)
class Schema:
    tables: FrozenDict[TableId, Table]
