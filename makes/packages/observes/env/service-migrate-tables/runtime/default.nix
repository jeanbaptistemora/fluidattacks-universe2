{ makes
, makeTemplate
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
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-service-migrate-tables-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      postgres-client.runtime
    ];
  };
}
