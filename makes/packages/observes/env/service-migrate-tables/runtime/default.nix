{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.service-migrate-tables;
  self = buildPythonPackage {
    name = "observes-service-migrate-tables";
    packagePath = path "/observes/services/migrate_tables";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-service-migrate-tables-runtime";
  searchPaths = {
    envSources = [
      env.runtime.postgres-client
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}
