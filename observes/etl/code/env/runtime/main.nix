{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-etl-code-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
