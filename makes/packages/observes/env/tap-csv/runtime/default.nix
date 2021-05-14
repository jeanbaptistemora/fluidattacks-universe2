{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_csv";
in
makeTemplate {
  name = "observes-env-tap-csv-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-csv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-csv.runtime.python
    ];
    envSources = [
      singer-io.runtime
    ];
  };
}
