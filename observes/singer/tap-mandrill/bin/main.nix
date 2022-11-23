{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.mandrill.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "tap-mandrill";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
