{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_checkly";
in
makeTemplate {
  name = "observes-env-tap-checkly-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-checkly.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-checkly.runtime.python
    ];
    envSources = [
      paginator.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}
