{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/streamer_dynamodb";
in
makeTemplate {
  name = "observes-env-streamer-dynamodb-runtime";
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
