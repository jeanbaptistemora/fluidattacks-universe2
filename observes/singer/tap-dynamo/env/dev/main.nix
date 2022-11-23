{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.dynamo.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-singer-tap-dynamo-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
