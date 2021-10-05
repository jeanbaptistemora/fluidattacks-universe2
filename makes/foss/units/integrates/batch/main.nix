{ inputs
, makeScript
, outputs
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
      inputs.nixpkgs.python39
      inputs.product.integrates-storage
      outputs."/integrates/cache"
      outputs."/integrates/db"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/batch/entrypoint.sh";
}
