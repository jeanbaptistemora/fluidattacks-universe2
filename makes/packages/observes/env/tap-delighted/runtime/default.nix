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
      env.paginator.runtime
      env.singer-io.runtime
      env.utils-logger.runtime
    ];
  };
}
