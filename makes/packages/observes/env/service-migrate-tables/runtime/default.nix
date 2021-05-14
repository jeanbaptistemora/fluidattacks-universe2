{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/services/migrate_tables";
in
makeTemplate {
  name = "observes-env-service-migrate-tables-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      service-migrate-tables.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      service-migrate-tables.runtime.python
    ];
    envSources = [
      postgres-client.runtime
    ];
  };
}
