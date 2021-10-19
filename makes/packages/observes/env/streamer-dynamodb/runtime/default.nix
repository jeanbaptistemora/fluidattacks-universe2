{ makes
, makeTemplate
, path
, ...
}:
let
  self = path "/observes/singer/streamer_dynamodb";
in
makeTemplate {
  name = "observes-env-streamer-dynamodb-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        withWheel_0_37_0 = true;
        withSetuptools_57_4_0 = true;
        name = "observes-env-streamer-dynamodb-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
