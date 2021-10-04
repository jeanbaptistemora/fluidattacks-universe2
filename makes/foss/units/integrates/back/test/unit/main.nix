{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
    __argBatchBin__ = "${inputs.product.integrates-batch}/bin/integrates-batch";
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    source = [
      inputs.product.integrates-back-pypi-unit-tests
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/back/test/unit/entrypoint.sh";
}
