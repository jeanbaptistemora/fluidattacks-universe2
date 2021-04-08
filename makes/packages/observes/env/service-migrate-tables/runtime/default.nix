{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.service-migrate-tables;
  self = path "/observes/services/migrate_tables";
in
makeTemplate {
  name = "observes-env-service-migrate-tables-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
    ];
    envSources = [
      env.runtime.postgres-client
    ];
  };
}
