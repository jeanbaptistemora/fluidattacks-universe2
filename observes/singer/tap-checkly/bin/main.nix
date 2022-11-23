{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.checkly.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.bin;
in
  makeScript {
    name = "tap-checkly";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
