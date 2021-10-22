{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/services/migrate_tables";
in
makeTemplate {
  name = "observes-env-service-migrate-tables-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-service-migrate-tables-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/postgres-client/runtime"
    ];
  };
}
