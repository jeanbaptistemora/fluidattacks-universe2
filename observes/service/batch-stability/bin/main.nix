{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.batch_stability.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "observes-batch-stability";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
