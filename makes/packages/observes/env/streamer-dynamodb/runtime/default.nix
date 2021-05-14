{ makeTemplate
, path
, packages
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/streamer_dynamodb";
in
makeTemplate {
  name = "observes-env-streamer-dynamodb-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      streamer-dynamodb.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      streamer-dynamodb.runtime.python
    ];
  };
}
