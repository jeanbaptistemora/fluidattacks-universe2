# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_migration import (
    my_exporter,
)
from db_migration.creds import (
    EnvVarPrefix,
    from_env,
)

my_exporter(from_env(EnvVarPrefix.SOURCE), from_env(EnvVarPrefix.TARGET)).bind(
    lambda e: e.migrate()
).compute()
