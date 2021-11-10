{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "check-forces-output";
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesSecrets__ = projectPath "/integrates";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.coreutils
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/forces"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
