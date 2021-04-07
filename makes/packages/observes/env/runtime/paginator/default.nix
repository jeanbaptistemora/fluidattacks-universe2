{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.runtime.paginator;
  self = path "/observes/common/paginator";
in
makeTemplate {
  name = "observes-env-runtime-paginator";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      pkgEnv.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.python
    ];
  };
}
