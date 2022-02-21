{ inputs
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.utils_logger.root;
  pkg = (inputs.flakeAdapter { src = self; }).defaultNix;
  env = pkg.outputs.packages.x86_64-linux.env.runtime;
in
makeTemplate {
  name = "observes-common-utils-logger-env-runtime";
  searchPaths = {
    bin = [ env ];
    pythonPackage = [
      self
    ];
  };
}
