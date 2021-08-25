{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_checkly";
in
makeTemplate {
  name = "observes-env-tap-checkly-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-checkly-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.paginator.runtime
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}
