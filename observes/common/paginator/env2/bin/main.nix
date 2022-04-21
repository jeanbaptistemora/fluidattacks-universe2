{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/observes/common/paginator";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-common-paginator-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
