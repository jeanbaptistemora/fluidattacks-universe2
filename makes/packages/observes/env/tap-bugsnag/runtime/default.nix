{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_bugsnag";
in
makeTemplate {
  name = "observes-env-tap-bugsnag-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-bugsnag.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-bugsnag.runtime.python
    ];
    envSources = [
      paginator.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}
