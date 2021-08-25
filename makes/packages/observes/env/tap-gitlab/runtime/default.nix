{ makes
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "observes-env-tap-gitlab-runtime";
  searchPaths = {
    envPythonPaths = [
      (path "/observes/singer/tap_gitlab")
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-gitlab-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.paginator.runtime
      packages.observes.env.postgres-client.runtime
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}
