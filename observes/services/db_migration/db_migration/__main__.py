from db_migration import (
    EnvVarPrefix,
    from_env,
    main,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.pure_iter.transform import (
    consume,
)

main(from_env(EnvVarPrefix.SOURCE), from_env(EnvVarPrefix.TARGET)).bind(
    lambda e: e.target_tables()
).bind(
    lambda p: consume(p.map(lambda i: Cmd.from_cmd(lambda: print(i))))
).compute()
