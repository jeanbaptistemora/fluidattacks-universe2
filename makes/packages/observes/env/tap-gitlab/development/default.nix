{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-gitlab-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-gitlab-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.tap-gitlab.runtime
    ];
  };
}
