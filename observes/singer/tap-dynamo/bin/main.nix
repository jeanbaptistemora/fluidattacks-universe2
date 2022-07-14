{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.dynamo.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.bin;
in
  makeScript {
    entrypoint = ''
      tap-dynamo "$@"
    '';
    searchPaths = {
      bin = [
        env
      ];
    };
    name = "observes-singer-tap-dynamo-bin";
  }
