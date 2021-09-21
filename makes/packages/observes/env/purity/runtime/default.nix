{ makes
, makeTemplate
, path
, ...
}:
let
  self = path "/observes/common/purity";
in
makeTemplate {
  name = "observes-env-purity-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-purity-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
