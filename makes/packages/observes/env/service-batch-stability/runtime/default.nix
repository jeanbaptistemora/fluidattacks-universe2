{ makes
, makeTemplate
, path
, ...
}:
let
  self = path "/observes/services/batch_stability";
in
makeTemplate {
  name = "observes-env-runtime-batch-stability";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-runtime-batch-stability";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
