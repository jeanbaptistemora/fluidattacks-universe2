{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-code-etl-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-code-etl-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.code-etl.runtime
    ];
  };
}
