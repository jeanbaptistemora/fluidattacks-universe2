{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  name = "integrates-batch";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python37
      inputs.product.integrates-db
      inputs.product.integrates-cache
      inputs.product.integrates-storage
    ];
    source = [
      (inputs.legacy.importUtility "aws")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/batch/entrypoint.sh";
}
