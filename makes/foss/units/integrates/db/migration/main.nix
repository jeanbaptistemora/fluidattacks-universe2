{ makeScript
, projectPath
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-db-migration";
  entrypoint = projectPath "/makes/foss/units/integrates/db/migration/entrypoint.sh";
}
