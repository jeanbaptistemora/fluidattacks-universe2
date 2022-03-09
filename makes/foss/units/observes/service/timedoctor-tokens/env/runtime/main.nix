{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath "/observes/services/timedoctor_tokens";
in
  makeTemplate {
    name = "observes-service-timedoctor-tokens-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      bin = [
        outputs."/observes/common/update-project-variable/bin"
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-service-timedoctor-tokens-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
