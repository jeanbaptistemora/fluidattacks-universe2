{ inputs
, makeScript
, projectPath
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-scheduler";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python37
      inputs.product.melts
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/scheduler/entrypoint.sh";
}
