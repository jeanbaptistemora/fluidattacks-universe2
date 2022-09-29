# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity.json.primitive import (
    Primitive,
)
from target_snowflake.snowflake_client.data_type import (
    DataType,
)


@dataclass(frozen=True)
class Column:
    data_type: DataType
    nullable: bool
    default: Primitive
