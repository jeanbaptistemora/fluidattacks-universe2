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
