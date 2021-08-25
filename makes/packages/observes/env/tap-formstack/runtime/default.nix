{ makes
, makeTemplate
, path
, ...
}:
let
  self = path "/observes/singer/tap_formstack";
in
makeTemplate {
  name = "observes-env-tap-formstack-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-formstack-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
