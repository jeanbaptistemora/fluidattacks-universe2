# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
)
from target_snowflake.snowflake_client.schema import (
    Schema,
)
from target_snowflake.snowflake_client.sql_client import (
    Identifier,
)


@dataclass(frozen=True)
class SchemaId:
    name: Identifier


@dataclass(frozen=True)
class Database:
    tables: FrozenDict[SchemaId, Schema]
