{
  inputs,
  makeTemplate,
  projectPath,
  fetchNixpkgs,
  ...
}: let
  root = projectPath inputs.observesIndex.service.db_migration.root;
  pkg = import "${root}/main.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-service-db-migration-env-development";
  }
