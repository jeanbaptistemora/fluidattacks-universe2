{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-charts-documents";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.python39
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
    source = [
      outputs."/integrates/back/charts/pypi"
      outputs."/utils/aws"
      outputs."/utils/common"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
