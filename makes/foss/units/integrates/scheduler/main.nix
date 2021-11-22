{ inputs
, makeScript
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
  entrypoint = ./entrypoint.sh;
}
