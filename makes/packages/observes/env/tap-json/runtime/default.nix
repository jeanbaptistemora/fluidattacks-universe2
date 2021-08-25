{ makeTemplate
, makes
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_json";
in
makeTemplate {
  name = "observes-env-tap-json-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-json-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}
