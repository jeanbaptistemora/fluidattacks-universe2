{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_bugsnag";
in
makeTemplate {
  name = "observes-env-tap-bugsnag-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-bugsnag-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.paginator.runtime
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}
