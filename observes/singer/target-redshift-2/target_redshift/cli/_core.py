# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import click
from dataclasses import (
    dataclass,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
    creds: Credentials


pass_ctx = click.make_pass_decorator(CmdContext)
