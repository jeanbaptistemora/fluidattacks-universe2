{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/services/batch_stability";
in
makeTemplate {
  name = "observes-service-batch-stability-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-service-batch-stability-env-runtime-python";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
