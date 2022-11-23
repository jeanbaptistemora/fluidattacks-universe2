{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.common.purity;
in
  makeTemplate {
    name = "observes-common-purity-env-runtime";
    searchPaths = {
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-common-purity-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
      ];
    };
  }
