{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_formstack";
in
makeTemplate {
  name = "observes-env-tap-formstack-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-formstack.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-formstack.runtime.python
    ];
  };
}
