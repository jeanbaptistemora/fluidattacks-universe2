{ makeTemplate
, path
, packages
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_zoho_analytics";
in
makeTemplate {
  name = "observes-env-tap-zoho-analytics-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-zoho-analytics.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-zoho-analytics.runtime.python
    ];
  };
}
