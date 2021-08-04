{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_announcekit";
in
makeTemplate {
  name = "observes-env-tap-announcekit-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-announcekit.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-announcekit.runtime.python
    ];
    envSources = [
      paginator.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}
