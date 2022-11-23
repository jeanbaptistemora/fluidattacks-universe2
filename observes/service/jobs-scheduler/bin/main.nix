{
  fetchNixpkgs,
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "observes-scheduler";
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."${inputs.observesIndex.service.scheduler.env.runtime}"
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
