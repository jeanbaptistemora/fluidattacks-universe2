{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-postgres-client-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-postgres-client-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/postgres-client/runtime"
    ];
  };
}
