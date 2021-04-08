{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.utils-logger;
  self = path "/observes/common/utils_logger";
in
makeTemplate {
  name = "observes-env-utils-logger-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
    ];
  };
}
