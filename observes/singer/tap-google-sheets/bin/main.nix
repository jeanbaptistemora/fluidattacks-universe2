{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs;
  };
  env = pkg.env.bin;
in
  makeScript {
    name = "tap-google-sheets";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ''
      tap-google-sheets "$@"
    '';
  }
