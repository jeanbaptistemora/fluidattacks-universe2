{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "sorts-association-rules-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
