# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from snowflake.connector.cursor import (
    SnowflakeCursor,
)


@dataclass(frozen=True)
class RawCursor:
    cursor: SnowflakeCursor
