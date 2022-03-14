from db_migration import (
    my_exporter,
    PENDING_IMPORT,
)
from db_migration.creds import (
    EnvVarPrefix,
    from_env,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)

my_exporter(from_env(EnvVarPrefix.SOURCE), from_env(EnvVarPrefix.TARGET)).bind(
    lambda e: e.import_from_s3(from_flist(PENDING_IMPORT))
).compute()
