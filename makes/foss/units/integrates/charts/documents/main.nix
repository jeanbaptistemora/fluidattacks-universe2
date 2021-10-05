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
  name = "integrates-charts-documents";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.python39
      inputs.product.integrates-storage
      outputs."/integrates/cache"
      outputs."/integrates/db"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/charts/documents/entrypoint.sh";
}
