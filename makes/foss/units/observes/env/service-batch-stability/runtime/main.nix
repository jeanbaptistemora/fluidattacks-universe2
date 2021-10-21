{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/services/batch_stability";
in
makeTemplate {
  name = "observes-env-runtime-batch-stability";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-runtime-batch-stability";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
