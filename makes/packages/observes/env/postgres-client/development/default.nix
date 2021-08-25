{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-postgres-client-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-postgres-client-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.postgres-client.runtime
    ];
  };
}
