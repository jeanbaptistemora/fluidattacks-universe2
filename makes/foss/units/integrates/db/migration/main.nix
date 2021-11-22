{ makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-db-migration";
  entrypoint = ./entrypoint.sh;
}
