{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "sorts-association-rules-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
