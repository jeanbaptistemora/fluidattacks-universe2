{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-common-postgres-client-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-postgres-client-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/postgres-client/env/runtime"
    ];
  };
}
