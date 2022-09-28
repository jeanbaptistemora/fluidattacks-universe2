# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from target_snowflake.db import (
    SchemaId,
)
from target_snowflake.schema import (
    TableId,
)
from target_snowflake.sql_client import (
    DatabaseId,
)


@dataclass(frozen=True)
class RemoteSchemaPointer:
    db: DatabaseId
    schema: SchemaId


@dataclass(frozen=True)
class RemoteTablePointer:
    db: DatabaseId
    schema: SchemaId
    table: TableId
