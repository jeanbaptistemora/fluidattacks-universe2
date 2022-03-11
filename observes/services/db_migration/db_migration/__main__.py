from db_migration import (
    EnvVarPrefix,
    from_env,
    main,
)

main(from_env(EnvVarPrefix.SOURCE), from_env(EnvVarPrefix.TARGET)).bind(
    lambda e: e.export_to_s3()
).compute()
