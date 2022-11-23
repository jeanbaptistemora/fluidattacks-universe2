{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.checkly.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-singer-tap-checkly-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
