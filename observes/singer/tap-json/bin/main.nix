{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.json.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.bin;
in
  makeScript {
    name = "tap-json";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ''
      tap-json "$@"
    '';
  }
