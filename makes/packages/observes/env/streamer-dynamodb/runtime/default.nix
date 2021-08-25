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
        name = "observes-env-streamer-dynamodb-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
