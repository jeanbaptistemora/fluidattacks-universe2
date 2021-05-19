{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/target_redshift";
in
makeTemplate {
  name = "observes-env-target-redshift-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      target-redshift.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      target-redshift.runtime.python
    ];
  };
}
