{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.s3.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "target-s3";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
