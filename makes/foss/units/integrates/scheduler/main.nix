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
      inputs.nixpkgs.python39
      outputs."/melts"
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/scheduler/entrypoint.sh";
}
