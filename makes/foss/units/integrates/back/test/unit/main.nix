{ makeScript
, inputs
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    bin = [
      outputs."/integrates/batch"
      outputs."/integrates/cache"
      inputs.product.integrates-db
      inputs.product.integrates-storage
    ];
    source = [
      inputs.product.integrates-back-pypi-unit-tests
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/back/test/unit/entrypoint.sh";
}
