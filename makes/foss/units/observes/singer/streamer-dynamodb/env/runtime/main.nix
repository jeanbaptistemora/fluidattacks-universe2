{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.streamer_dynamodb.root;
in
  makeTemplate {
    name = "observes-singer-streamer-dynamodb-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          withWheel_0_37_0 = true;
          withSetuptools_57_4_0 = true;
          name = "observes-env-streamer-dynamodb-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
      ];
    };
  }
