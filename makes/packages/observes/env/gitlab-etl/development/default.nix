{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-gitlab-etl-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-gitlab-etl-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.gitlab-etl.runtime
    ];
  };
}
