{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_delighted";
in
makeTemplate {
  name = "observes-env-tap-delighted-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-delighted.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-delighted.runtime.python
    ];
    envSources = [
      paginator.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}
