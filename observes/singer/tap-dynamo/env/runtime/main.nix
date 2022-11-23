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
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-tap-dynamo-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
