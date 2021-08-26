{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-paginator-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-paginator-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.paginator.runtime
    ];
  };
}
