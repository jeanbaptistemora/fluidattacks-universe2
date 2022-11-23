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
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-tap-checkly-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
