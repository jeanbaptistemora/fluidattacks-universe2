# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import click
from dataclasses import (
    dataclass,
)
from target_snowflake.snowflake_client.sql_client import (
    Credentials,
    DatabaseId,
)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
    creds: Credentials


pass_ctx = click.make_pass_decorator(CmdContext)  # type: ignore[misc]
