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
    envMypy38Paths = [
      self
    ];
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}
