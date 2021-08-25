{ makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/common/utils_logger";
in
makeTemplate {
  name = "observes-env-utils-logger-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      packages.observes.env.utils-logger.runtime.python
    ];
  };
}
