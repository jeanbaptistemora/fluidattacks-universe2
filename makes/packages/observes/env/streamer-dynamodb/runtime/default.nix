{ makeTemplate
, path
, packages
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.streamer-dynamodb;
  self = path "/observes/singer/streamer_dynamodb";
in
makeTemplate {
  name = "observes-env-streamer-dynamodb-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}
