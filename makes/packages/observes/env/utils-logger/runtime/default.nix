{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pkgEnv = packages.observes.env;
  pythonRunReqs = pkgEnv.utils-logger.runtime.python;
  self = buildPythonPackage {
    name = "observes-utils-logger";
    packagePath = path "/observes/common/utils_logger";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-utils-logger-runtime";
  searchPaths = {
    envPython38Paths = [
      pythonRunReqs
      self
    ];
    envMypy38Paths = [
      self
    ];
  };
}
