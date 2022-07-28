{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-back-lint-schema-deprecations";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
}
