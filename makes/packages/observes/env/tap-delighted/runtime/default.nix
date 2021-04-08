{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-delighted;
  self = path "/observes/singer/tap_delighted";
in
makeTemplate {
  name = "observes-env-tap-delighted-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
    ];
    envSources = [
      env.runtime.paginator
      env.runtime.singer-io
      env.utils-logger.runtime
    ];
  };
}
