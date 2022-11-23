{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.gitlab.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "tap-gitlab";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
