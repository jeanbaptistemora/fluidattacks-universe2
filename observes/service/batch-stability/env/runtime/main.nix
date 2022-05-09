{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.service.batch_stability.root;
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
