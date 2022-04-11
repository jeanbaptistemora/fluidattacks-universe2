{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-etl-code-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
