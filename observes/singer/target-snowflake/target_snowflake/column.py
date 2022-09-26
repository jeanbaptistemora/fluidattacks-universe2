# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity.json.primitive import (
    Primitive,
)
from target_snowflake.data_type import (
    DataType,
)
from target_snowflake.sql_client import (
    Identifier,
)


@dataclass(frozen=True)
class ColumnId:
    name: Identifier


@dataclass(frozen=True)
class Column:
    data_type: DataType
    primary_key: bool
    unique_key: bool
    nullable: bool
    default: Primitive


@dataclass(frozen=True)
class ColumnObj:
    id_obj: ColumnId
    column: Column
