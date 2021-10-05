{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  name = "integrates-db-migration";
  entrypoint = projectPath "/makes/foss/units/integrates/db/migration/entrypoint.sh";
}
