{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-batch";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/melts"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "env")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/batch/entrypoint.sh";
}
