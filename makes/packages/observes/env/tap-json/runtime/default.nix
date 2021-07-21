{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_json";
in
makeTemplate {
  name = "observes-env-tap-json-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-json.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-json.runtime.python
    ];
    envSources = [
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}
