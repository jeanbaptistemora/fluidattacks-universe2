{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/common/utils_logger";
in
makeTemplate {
  name = "observes-env-utils-logger-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      utils-logger.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      utils-logger.runtime.python
    ];
  };
}
