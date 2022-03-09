{
  inputs,
  makeTemplate,
  projectPath,
  fetchNixpkgs,
  ...
}: let
  root = projectPath inputs.observesIndex.common.utils_logger.root;
  pkg = import "${root}/main.nix" fetchNixpkgs;
  env = pkg.env.dev;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-common-utils-logger-new-env-development";
  }
