{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.bin;
in
  makeScript {
    name = "observes-etl-code";
    searchPaths = {
      bin = [
        env
        inputs.nixpkgs.git
      ];
    };
    entrypoint = ''
      observes-etl-code "$@"
    '';
  }
