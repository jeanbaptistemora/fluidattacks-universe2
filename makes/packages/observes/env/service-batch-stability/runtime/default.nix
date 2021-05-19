{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/services/batch_stability";
in
makeTemplate {
  name = "observes-env-runtime-batch-stability";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      service-batch-stability.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      service-batch-stability.runtime.python
    ];
  };
}
